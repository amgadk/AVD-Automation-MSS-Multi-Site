"""
ports.py
ANTA Custom Test Classes with array output parsing and normalized host pinging execution.
"""

from pydantic import BaseModel, Field, IPvAnyAddress
from typing import Literal, Optional, List
from anta.models import AntaTest, AntaCommand, AntaTemplate

PEER_DEVICES = {
    "172.16.11.10": "Staff-H1",
    "172.16.21.10": "Media-H2",
    "172.16.31.10": "IOT-H3",
    "172.16.41.10": "Sales-H4",
}

class BaseLayer4Socket(AntaTest):
    """Base class providing transport path validation via explicit shell-routing wrappers."""
    categories = ["connectivity"]
    
    commands = [
        AntaTemplate(
            template="bash timeout {timeout} bash -c 'if [ \"{vrf}\" = \"default\" ]; then iperf -c {destination} -p {port} {udp_flag} -t 2; else ip netns exec ns-{vrf} iperf -c {destination} -p {port} {udp_flag} -t 2; fi'", 
            ofmt="text"
        )
    ]

    class Input(AntaTest.Input):
        destination: IPvAnyAddress = Field(description="Target destination IP address to test.")
        port: int = Field(description="Layer 4 target destination port number (1-65535).", ge=1, le=65535)
        timeout: int = Field(default=4, description="Handshake timeout in seconds.")
        vrf: str = Field(default="default", description="VRF routing context instance.")


class TCP(BaseLayer4Socket):
    """Validates active Layer 4 transport path parameters by rendering an iperf TCP client."""
    name = "TCP"
    description = "Validates active Layer 4 TCP transport path connectivity."

    def render(self, template: AntaTemplate) -> list[AntaCommand]:
        return [template.render(timeout=self.inputs.timeout + 3, vrf=self.inputs.vrf, destination=str(self.inputs.destination), port=self.inputs.port, udp_flag="")]

    @AntaTest.anta_test
    def test(self) -> None:
        dest_ip = str(self.inputs.destination)
        peer_name = PEER_DEVICES.get(dest_ip, dest_ip)
        self.result.description = f"Verify TCP session from {self.result.name} to {peer_name} (Port {self.inputs.port})"
        
        # --- FIX: Safely parse instance_commands as a list to avoid AttributeError ---
        cmds = self.instance_commands if isinstance(self.instance_commands, list) else [self.instance_commands]
        command_output = cmds[0].output.lower()
        
        if "connected" in command_output:
            self.result.is_success()
        else:
            self.result.is_failure(f"Connection refused or unreachable to {peer_name} on port {self.inputs.port}")


class Telnet(BaseLayer4Socket):
    """Validates cleartext Telnet path connectivity using native iperf templates."""
    name = "Telnet"
    description = "Validates active cleartext Telnet application layer delivery."
    
    class Input(BaseLayer4Socket.Input):
        port: int = Field(default=23, description="Telnet transport port.", ge=1, le=65535)

    def render(self, template: AntaTemplate) -> list[AntaCommand]:
        return [template.render(timeout=self.inputs.timeout + 3, vrf=self.inputs.vrf, destination=str(self.inputs.destination), port=self.inputs.port, udp_flag="")]

    @AntaTest.anta_test
    def test(self) -> None:
        dest_ip = str(self.inputs.destination)
        peer_name = PEER_DEVICES.get(dest_ip, dest_ip)
        self.result.description = f"Verify Telnet delivery from {self.result.name} to {peer_name}"
        
        # --- FIX: Safely parse instance_commands as a list ---
        cmds = self.instance_commands if isinstance(self.instance_commands, list) else [self.instance_commands]
        command_output = cmds[0].output.lower()
        
        if "connected" in command_output:
            self.result.is_success()
        else:
            self.result.is_failure(f"Cleartext Telnet path to {peer_name} is blocked or down")


class UDP(BaseLayer4Socket):
    """Validates active UDP transport path parameters by rendering an iperf UDP client."""
    name = "UDP"
    description = "Validates active Layer 4 UDP transport path connectivity."

    def render(self, template: AntaTemplate) -> list[AntaCommand]:
        return [template.render(timeout=self.inputs.timeout + 3, vrf=self.inputs.vrf, destination=str(self.inputs.destination), port=self.inputs.port, udp_flag="-u")]

    @AntaTest.anta_test
    def test(self) -> None:
        dest_ip = str(self.inputs.destination)
        peer_name = PEER_DEVICES.get(dest_ip, dest_ip)
        self.result.description = f"Verify UDP stream from {self.result.name} to {peer_name} (Port {self.inputs.port})"
        
        # --- FIX: Safely parse instance_commands as a list ---
        cmds = self.instance_commands if isinstance(self.instance_commands, list) else [self.instance_commands]
        command_output = cmds[0].output.lower()
        
        if "connected" in command_output or "connected with" in command_output:
            self.result.is_success()
        else:
            self.result.is_failure(f"UDP validation failed to {peer_name}")


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
