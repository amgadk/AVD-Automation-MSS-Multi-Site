"""
Custom ANTA test extension package exporting static name attributes.
"""
from .ports import TCP, UDP, Telnet, ICMP

__all__ = ["TCP", "UDP", "Telnet", "ICMP"]
