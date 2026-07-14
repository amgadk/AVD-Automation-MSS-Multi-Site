"""
ports.py
ANTA Custom Test Classes with array output parsing and normalized host pinging execution.
"""

from pydantic import BaseModel, Field, IPvAnyAddress
from typing import Literal, Optional, List
from anta.models import AntaTest, AntaCommand, AntaTemplate

PEER_DEVICES = {
    "172.16.11.10": "c1-Staff-H1",
    "172.16.21.10": "c1-Media-H2",
    "172.16.31.10": "c1-IOT-H3",
    "172.16.41.10": "c1-Sales-H4",
    "172.16.12.10": "c2-Staff-H1",
    "172.16.22.10": "c2-Media-H2",
    "172.16.32.10": "c2-IOT-H3",
    "172.16.42.10": "c2-Sales-H4",
    "172.16.13.10": "c3-Staff-H1",
    "172.16.23.10": "c3-Media-H2",
    "172.16.33.10": "c3-IOT-H3",
    "172.16.43.10": "c3-Sales-H4",
}

class TCP(AntaTest):
    """Validates Layer 4 TCP reachability by opening a raw /dev/tcp socket and checking for
    an SSH identification banner. Relies on sshd, which already runs by default on every EOS
    host, so no test server needs to be deployed on the destination."""
    name = "TCP"
    description = "Validates active Layer 4 TCP connectivity via SSH banner exchange (port 22)."
    categories = ["connectivity"]

    commands = [
        AntaTemplate(
            template="bash timeout {timeout} bash -c 'if [ \"{vrf}\" = \"default\" ]; then cat < /dev/tcp/{destination}/{port}; else ip netns exec ns-{vrf} bash -c \"cat < /dev/tcp/{destination}/{port}\"; fi'",
            ofmt="text"
        )
    ]

    class Input(AntaTest.Input):
        destination: IPvAnyAddress = Field(description="Target destination IP address to test.")
        port: int = Field(default=22, description="TCP destination port (defaults to SSH).", ge=1, le=65535)
        timeout: int = Field(default=3, description="Connection timeout in seconds.")
        vrf: str = Field(default="default", description="VRF routing context instance.")

    def render(self, template: AntaTemplate) -> list[AntaCommand]:
        return [template.render(timeout=self.inputs.timeout, vrf=self.inputs.vrf, destination=str(self.inputs.destination), port=self.inputs.port)]

    @AntaTest.anta_test
    def test(self) -> None:
        dest_ip = str(self.inputs.destination)
        peer_name = PEER_DEVICES.get(dest_ip, dest_ip)
        self.result.description = f"Verify TCP/SSH reachability from {self.result.name} to {peer_name} (Port {self.inputs.port})"

        cmds = self.instance_commands if isinstance(self.instance_commands, list) else [self.instance_commands]
        command_output = cmds[0].output.lower()

        if "ssh-" in command_output:
            self.result.is_success()
        else:
            self.result.is_failure(f"No SSH banner received from {peer_name} on port {self.inputs.port} - port closed or unreachable")


class Telnet(AntaTest):
    """Validates cleartext Telnet (port 23) reachability by opening a raw /dev/tcp socket.
    Unlike SSH, Telnet servers reply with binary IAC negotiation bytes rather than a clean
    text banner, so success is inferred from receiving any data at all without an explicit
    refusal - rather than matching specific banner text. Output is piped through `cat -v`
    since those raw IAC bytes otherwise corrupt the eAPI JSON-RPC response and crash the
    client with a bare KeyError instead of a normal command error.
    Requires 'management telnet' / 'no shutdown' on the destination (added to the department
    representative hosts in host_configs/*.cfg - it is not an EOS default, unlike sshd)."""
    name = "Telnet"
    description = "Validates active cleartext Telnet (port 23) reachability."
    categories = ["connectivity"]

    commands = [
        AntaTemplate(
            template="bash timeout {timeout} bash -c 'if [ \"{vrf}\" = \"default\" ]; then cat < /dev/tcp/{destination}/{port} | cat -v; else ip netns exec ns-{vrf} bash -c \"cat < /dev/tcp/{destination}/{port} | cat -v\"; fi'",
            ofmt="text"
        )
    ]

    class Input(AntaTest.Input):
        destination: IPvAnyAddress = Field(description="Target destination IP address to test.")
        port: int = Field(default=23, description="Telnet destination port.", ge=1, le=65535)
        timeout: int = Field(default=3, description="Connection timeout in seconds.")
        vrf: str = Field(default="default", description="VRF routing context instance.")

    def render(self, template: AntaTemplate) -> list[AntaCommand]:
        return [template.render(timeout=self.inputs.timeout, vrf=self.inputs.vrf, destination=str(self.inputs.destination), port=self.inputs.port)]

    @AntaTest.anta_test
    def test(self) -> None:
        dest_ip = str(self.inputs.destination)
        peer_name = PEER_DEVICES.get(dest_ip, dest_ip)
        self.result.description = f"Verify Telnet reachability from {self.result.name} to {peer_name} (Port {self.inputs.port})"

        cmds = self.instance_commands if isinstance(self.instance_commands, list) else [self.instance_commands]
        raw_output = cmds[0].output
        command_output = raw_output.lower()
        refused = any(kw in command_output for kw in ("refused", "unreachable", "no route"))

        if raw_output.strip() and not refused:
            self.result.is_success()
        else:
            self.result.is_failure(f"Telnet port {self.inputs.port} on {peer_name} did not respond - closed, unreachable, or filtered")


class UDP(AntaTest):
    """Fire-and-forget UDP reachability probe: sends an empty datagram via a raw /dev/udp
    socket and checks that the local send succeeded (routable, no immediate socket error).
    UDP has no handshake, so this does NOT confirm anything is listening on the destination
    port - it only confirms the datagram could be sent along the path."""
    name = "UDP"
    description = "Validates that a UDP datagram can be sent to the destination:port (send-only, no listener confirmation)."
    categories = ["connectivity"]

    commands = [
        AntaTemplate(
            template="bash timeout {timeout} bash -c 'if [ \"{vrf}\" = \"default\" ]; then (echo -n | cat > /dev/udp/{destination}/{port}) && echo UDP_SEND_OK || echo UDP_SEND_FAIL; else ip netns exec ns-{vrf} bash -c \"(echo -n | cat > /dev/udp/{destination}/{port}) && echo UDP_SEND_OK || echo UDP_SEND_FAIL\"; fi'",
            ofmt="text"
        )
    ]

    class Input(AntaTest.Input):
        destination: IPvAnyAddress = Field(description="Target destination IP address to test.")
        port: int = Field(default=53, description="UDP destination port (defaults to DNS).", ge=1, le=65535)
        timeout: int = Field(default=3, description="Send timeout in seconds.")
        vrf: str = Field(default="default", description="VRF routing context instance.")

    def render(self, template: AntaTemplate) -> list[AntaCommand]:
        return [template.render(timeout=self.inputs.timeout, vrf=self.inputs.vrf, destination=str(self.inputs.destination), port=self.inputs.port)]

    @AntaTest.anta_test
    def test(self) -> None:
        dest_ip = str(self.inputs.destination)
        peer_name = PEER_DEVICES.get(dest_ip, dest_ip)
        self.result.description = f"Verify UDP datagram send path from {self.result.name} to {peer_name} (Port {self.inputs.port})"

        cmds = self.instance_commands if isinstance(self.instance_commands, list) else [self.instance_commands]
        command_output = cmds[0].output.lower()

        if "udp_send_ok" in command_output:
            self.result.is_success()
        else:
            self.result.is_failure(f"Unable to send UDP datagram to {peer_name} on port {self.inputs.port} (routing/socket error)")


# ==========================================
#  FIXED & STABILIZED ICMP EXTENSION MODULE
# ==========================================
class ICMP(AntaTest):
    """Validates connectivity via shell pinging templates to avoid token syntax rejections."""
    categories = ["connectivity"]
    name = "ICMP"
    description = "Test network reachability via standard ICMP echo."

    # --- FIX: Use a standardized ping command template that strips out unsupported VRF tokens for hosts ---
    commands = [AntaTemplate(template="ping {destination} repeat {repeat}", ofmt="text")]

    class Input(AntaTest.Input):
        class HostItem(BaseModel):
            destination: str
            vrf: str = "default"
            repeat: int = 5

        hosts: List[HostItem]

    def render(self, template: AntaTemplate) -> list[AntaCommand]:
        commands = []
        for host in self.inputs.hosts:
            commands.append(
                template.render(
                    destination=host.destination,
                    repeat=host.repeat
                )
            )
        return commands

    @AntaTest.anta_test
    def test(self) -> None:
        failures = []
        paths = []
        
        cmds = self.instance_commands if isinstance(self.instance_commands, list) else [self.instance_commands]
        
        for cmd in cmds:
            cmd_parts = cmd.command.split()
            # Extract target IP from the dynamic ping string index array
            dest_ip = cmd_parts[1] if len(cmd_parts) > 1 else "Unknown"
            
            peer_name = PEER_DEVICES.get(dest_ip, dest_ip)
            paths.append(f"{self.result.name} to {peer_name}")

            if "bytes from" not in cmd.output or "100% packet loss" in cmd.output:
                failures.append(f"Ping completely failed to target device: {peer_name}")

        self.result.description = f"ICMP reachability validation for: {', '.join(paths)}"

        if failures:
            self.result.is_failure("\n".join(failures))
        else:
            self.result.is_success()
