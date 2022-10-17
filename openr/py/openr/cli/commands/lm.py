#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import sys
from builtins import object
from typing import Any, Dict, List, Optional, Sequence

import click
from openr.cli.utils import utils
from openr.cli.utils.commands import OpenrCtrlCmd
from openr.KvStore import ttypes as kv_store_types
from openr.OpenrCtrl import OpenrCtrl
from openr.thrift.KvStore.thrift_types import InitializationEvent
from openr.Types import ttypes as openr_types
from openr.utils import ipnetwork, printing


class LMCmdBase(OpenrCtrlCmd):
    """
    Base class for LinkMonitor cmds. All of LinkMonitor cmd
    is spawn out of this.
    """

    def toggle_node_overload_bit(
        self, client: OpenrCtrl.Client, overload: bool, yes: bool = False
    ) -> None:
        """[Hard-Drain] Node level overload"""

        links = self.fetch_lm_links(client)
        host = links.thisNodeName
        print()

        if overload and links.isOverloaded:
            print("Node {} is already overloaded.\n".format(host))
            sys.exit(0)

        if not overload and not links.isOverloaded:
            print("Node {} is not overloaded.\n".format(host))
            sys.exit(0)

        action = "set overload bit" if overload else "unset overload bit"
        if not utils.yesno(
            "Are you sure to {} for node {} ?".format(action, host), yes
        ):
            print()
            return

        if overload:
            client.setNodeOverload()
        else:
            client.unsetNodeOverload()

        print("Successfully {}..\n".format(action))

    def toggle_link_overload_bit(
        self,
        client: OpenrCtrl.Client,
        overload: bool,
        interface: str,
        yes: bool = False,
    ) -> None:
        """[Hard-Drain] Link level overload"""

        links = self.fetch_lm_links(client)
        print()

        if interface not in links.interfaceDetails:
            print("No such interface: {}".format(interface))
            return

        if overload and links.interfaceDetails[interface].isOverloaded:
            print("Interface is already overloaded.\n")
            sys.exit(0)

        if not overload and not links.interfaceDetails[interface].isOverloaded:
            print("Interface is not overloaded.\n")
            sys.exit(0)

        action = "set overload bit" if overload else "unset overload bit"
        question_str = "Are you sure to {} for interface {} ?"
        if not utils.yesno(question_str.format(action, interface), yes):
            print()
            return

        if overload:
            client.setInterfaceOverload(interface)
        else:
            client.unsetInterfaceOverload(interface)

        print("Successfully {} for the interface.\n".format(action))

    def toggle_node_metric_inc(
        self, client: OpenrCtrl.Client, metric_inc: int, yes: bool = False
    ) -> None:
        """[Soft-Drain] Node level metric increment"""

        links = self.fetch_lm_links(client)
        host = links.thisNodeName

        # ATTN:
        #   - sys.exit(0) will NOT print out existing AdjacencyDatabase
        #   - return will print out existing AdjacencyDatabase
        if metric_inc < 0:
            print(f"Can't set negative node metric increment on: {host}")
            sys.exit(0)

        if metric_inc and links.nodeMetricIncrementVal == metric_inc:
            print(f"Node metric increment already set with: {metric_inc}. No-op.\n")
            return

        if not metric_inc and links.nodeMetricIncrementVal == 0:
            print(f"No node metric increment has been set on: {host}. No-op.\n")
            return

        action = "set node metric inc" if metric_inc else "unset node metric inc"
        question_str = "Are you sure to {} for node {} ?"
        if not utils.yesno(question_str.format(action, host), yes):
            sys.exit(0)

        if metric_inc:
            client.setNodeInterfaceMetricIncrement(metric_inc)
        else:
            client.unsetNodeInterfaceMetricIncrement()

        print(f"Successfully {action} for node {host}.\n")

    def toggle_link_metric_inc(
        self,
        client: OpenrCtrl.Client,
        interface: str,
        metric_inc: int,
        yes: bool,
    ) -> None:
        """[Soft-Drain] Link level metric increment"""

        links = self.fetch_lm_links(client)
        host = links.thisNodeName

        # ATTN:
        #   - sys.exit(0) will NOT print out existing AdjacencyDatabase
        #   - return will print out existing AdjacencyDatabase
        if metric_inc < 0:
            print(f"Can't set negative link metric increment on: {host}")
            sys.exit(0)

        if interface not in links.interfaceDetails:
            print(f"No such interface: {interface} on node: {host}")
            sys.exit(0)

        if (
            metric_inc
            and links.interfaceDetails[interface].linkMetricIncrementVal == metric_inc
        ):
            print(f"Link metric increment already set with: {metric_inc}. No-op.\n")
            return

        if (
            not metric_inc
            and links.interfaceDetails[interface].linkMetricIncrementVal == 0
        ):
            print(f"No link metric increment has been set on: {interface}. No-op.\n")
            return

        action = "set link metric inc" if metric_inc else "unset link metric inc"
        question_str = "Are you sure to {} for link {} on node {} ?"
        if not utils.yesno(question_str.format(action, interface, host), yes):
            sys.exit(0)

        if metric_inc:
            client.setInterfaceMetricIncrement(interface, metric_inc)
        else:
            client.unsetInterfaceMetricIncrement(interface)

        print(f"Successfully {action} for interface {interface} on node {host}.\n")

    def check_link_overriden(
        self, links: openr_types.DumpLinksReply, interface: str, metric: int
    ) -> Optional[bool]:
        """
        This function call will comapre the metricOverride in the following way:
        1) metricOverride NOT set -> return None;
        2) metricOverride set -> return True/False;
        """
        metricOverride = links.interfaceDetails[interface].metricOverride
        if not metricOverride:
            return None
        return metricOverride == metric

    def toggle_link_metric(
        self,
        client: OpenrCtrl.Client,
        override: bool,
        interface: str,
        metric: int,
        yes: bool,
    ) -> None:
        links = self.fetch_lm_links(client)
        print()

        if interface not in links.interfaceDetails:
            print("No such interface: {}".format(interface))
            return

        status = self.check_link_overriden(links, interface, metric)
        if not override and status is None:
            print("Interface hasn't been assigned metric override.\n")
            sys.exit(0)

        if override and status:
            print(
                "Interface: {} has already been set with metric: {}.\n".format(
                    interface, metric
                )
            )
            sys.exit(0)

        action = "set override metric" if override else "unset override metric"
        question_str = "Are you sure to {} for interface {} ?"
        if not utils.yesno(question_str.format(action, interface), yes):
            print()
            return

        if override:
            client.setInterfaceMetric(interface, metric)
        else:
            client.unsetInterfaceMetric(interface)

        print("Successfully {} for the interface.\n".format(action))

    def interface_info_to_dict(self, interface_info):
        def _update(interface_info_dict, interface_info):
            interface_info_dict.update(
                {
                    "networks": [
                        ipnetwork.sprint_prefix(prefix)
                        for prefix in interface_info.networks
                    ]
                }
            )

        return utils.thrift_to_dict(interface_info, _update)

    def interface_details_to_dict(self, interface_details):
        def _update(interface_details_dict, interface_details):
            interface_details_dict.update(
                {"info": self.interface_info_to_dict(interface_details.info)}
            )

        return utils.thrift_to_dict(interface_details, _update)

    def links_to_dict(self, links):
        def _update(links_dict, links):
            links_dict.update(
                {
                    "interfaceDetails": {
                        k: self.interface_details_to_dict(v)
                        for k, v in links.interfaceDetails.items()
                    }
                }
            )
            del links_dict["thisNodeName"]

        return utils.thrift_to_dict(links, _update)

    def print_links_json(self, links):
        links_dict = {links.thisNodeName: self.links_to_dict(links)}
        print(utils.json_dumps(links_dict))

    @classmethod
    def build_table_rows(cls, interfaces: Dict[str, object]) -> List[List[str]]:
        rows = []
        for (k, v) in sorted(interfaces.items()):
            raw_row = cls.build_table_row(k, v)
            addrs = raw_row[3]
            raw_row[3] = ""
            rows.append(raw_row)
            for addrStr in addrs:
                rows.append(["", "", "", addrStr])
        return rows

    @staticmethod
    def build_table_row(k: str, v: object) -> List[Any]:
        # pyre-fixme[16]: `object` has no attribute `metricOverride`.
        metric_override = v.metricOverride if v.metricOverride else ""
        # pyre-fixme[16]: `object` has no attribute `info`.
        if v.info.isUp:
            backoff_sec = int(
                # pyre-fixme[16]: `object` has no attribute `linkFlapBackOffMs`.
                (v.linkFlapBackOffMs if v.linkFlapBackOffMs else 0)
                / 1000
            )
            if backoff_sec == 0:
                state = "Up"
            elif not utils.is_color_output_supported():
                state = backoff_sec
            else:
                state = click.style("Hold ({} s)".format(backoff_sec), fg="yellow")
        else:
            state = (
                click.style("Down", fg="red")
                if utils.is_color_output_supported()
                else "Down"
            )
        # pyre-fixme[16]: `object` has no attribute `isOverloaded`.
        if v.isOverloaded:
            metric_override = (
                click.style("Overloaded", fg="red")
                if utils.is_color_output_supported()
                else "Overloaded"
            )
        addrs = []
        for prefix in v.info.networks:
            addrStr = ipnetwork.sprint_addr(prefix.prefixAddress.addr)
            addrs.append(addrStr)
        row = [k, state, metric_override, addrs]
        return row

    @classmethod
    def print_links_table(cls, interfaces, caption=None):
        """
        @param interfaces: dict<interface-name, InterfaceDetail>
        @param caption: Caption to show on table name
        """

        columns = ["Interface", "Status", "Metric Override", "Addresses"]
        rows = cls.build_table_rows(interfaces)

        print(printing.render_horizontal_table(rows, columns, caption))


class SetNodeOverloadCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        yes: bool = False,
        *args,
        **kwargs,
    ) -> None:
        self.toggle_node_overload_bit(client, True, yes)


class UnsetNodeOverloadCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        yes: bool = False,
        *args,
        **kwargs,
    ) -> None:
        self.toggle_node_overload_bit(client, False, yes)


class SetLinkOverloadCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        interface: str,
        yes: bool,
        *args,
        **kwargs,
    ) -> None:
        self.toggle_link_overload_bit(client, True, interface, yes)


class UnsetLinkOverloadCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        interface: str,
        yes: bool,
        *args,
        **kwargs,
    ) -> None:
        self.toggle_link_overload_bit(client, False, interface, yes)


class IncreaseNodeMetricCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        metric: str,
        yes: bool,
        *args,
        **kwargs,
    ) -> None:
        self.toggle_node_metric_inc(client, int(metric), yes)


class ClearNodeMetricCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        yes: bool,
        *args,
        **kwargs,
    ) -> None:
        self.toggle_node_metric_inc(client, 0, yes)


class IncreaseLinkMetricCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        interface: str,
        metric: str,
        yes: bool,
        *args,
        **kwargs,
    ) -> None:
        self.toggle_link_metric_inc(client, interface, int(metric), yes)


class ClearLinkMetricCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        interface: str,
        yes: bool,
        *args,
        **kwargs,
    ) -> None:
        self.toggle_link_metric_inc(client, interface, 0, yes)


# [TO BE DEPRECATED]
class SetLinkMetricCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        interface: str,
        metric: str,
        yes: bool,
        *args,
        **kwargs,
    ) -> None:
        self.toggle_link_metric(client, True, interface, int(metric), yes)


class UnsetLinkMetricCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        interface: str,
        yes: bool,
        *args,
        **kwargs,
    ) -> None:
        self.toggle_link_metric(client, False, interface, 0, yes)


class OverrideAdjMetricCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        node: str,
        interface: str,
        metric: str,
        yes: bool,
        *args,
        **kwargs,
    ) -> None:
        client.setAdjacencyMetric(interface, node, int(metric))


class ClearAdjMetricOverrideCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        node: str,
        interface: str,
        yes: bool,
        *args,
        **kwargs,
    ) -> None:
        client.unsetAdjacencyMetric(interface, node)


class LMAdjCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        nodes: set,
        json: bool,
        areas: Sequence[str] = (),
        *args,
        **kwargs,
    ) -> None:
        area_filters = OpenrCtrl.AdjacenciesFilter(selectAreas=set(areas))
        adj_dbs = client.getLinkMonitorAdjacenciesFiltered(area_filters)

        for adj_db in adj_dbs:
            if adj_db and adj_db.area and not json:
                click.secho(f"Area: {adj_db.area}", bold=True)
            # adj_db is built with ONLY one single (node, adjDb). Ignpre bidir option
            adjs_map = utils.adj_dbs_to_dict(
                {adj_db.thisNodeName: adj_db}, nodes, False, self.iter_dbs
            )
            if json:
                utils.print_json(adjs_map)
            else:
                utils.print_adjs_table(adjs_map, None, None)


class LMLinksCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        only_suppressed: bool,
        json: bool,
        *args,
        **kwargs,
    ) -> None:
        links = self.fetch_lm_links(client)
        if only_suppressed:
            links.interfaceDetails = {
                k: v for k, v in links.interfaceDetails.items() if v.linkFlapBackOffMs
            }
        if json:
            self.print_links_json(links)
        else:
            overload_status = None
            node_metric_inc_status = None
            if utils.is_color_output_supported():
                # [Hard-Drain]
                overload_color = "red" if links.isOverloaded else "green"
                overload_status = click.style(
                    "{}".format("YES" if links.isOverloaded else "NO"),
                    fg=overload_color,
                )
                # [Soft-Drain]
                node_metric_inc_color = (
                    "red" if links.nodeMetricIncrementVal > 0 else "green"
                )
                node_metric_inc_status = click.style(
                    "{}".format(links.nodeMetricIncrementVal),
                    fg=node_metric_inc_color,
                )
            else:
                overload_status = "YES" if links.isOverloaded else "NO"
                node_metric_inc_status = "{}".format(links.nodeMetricIncrementVal)

            caption = "Node Overload: {}, Node Metric Increment: {}".format(
                overload_status, node_metric_inc_status
            )
            self.print_links_table(links.interfaceDetails, caption)


class LMValidateCmd(LMCmdBase):
    def _run(
        self,
        client: OpenrCtrl.Client,
        *args,
        **kwargs,
    ) -> bool:

        is_pass = True

        # Get Data
        links = self.fetch_lm_links(client)
        initialization_events = self.fetch_initialization_events(client)
        openr_config = self.fetch_running_config_thrift(client)

        # Run the validation checks
        init_is_pass, init_err_msg_str, init_dur_str = self.validate_init_event(
            initialization_events,
            kv_store_types.InitializationEvent.LINK_DISCOVERED,
        )

        is_pass = is_pass and init_is_pass

        regex_invalid_interfaces = self._validate_interface_regex(
            links, openr_config.areas
        )

        is_pass = is_pass and (len(regex_invalid_interfaces) == 0)

        # Render Validation Results
        self.print_initialization_event_check(
            init_is_pass,
            init_err_msg_str,
            init_dur_str,
            InitializationEvent.LINK_DISCOVERED,
            "link monitor",
        )
        self._print_interface_validation_info(regex_invalid_interfaces)

        return is_pass

    def _validate_interface_regex(
        self, links: openr_types.DumpLinksReply, areas: List[Any]
    ) -> Dict[str, Any]:
        """
        Checks if each interface passes the regexes of atleast one area
        Returns a dictionary interface : interfaceDetails of the invalid interfaces
        """

        interfaces = list(links.interfaceDetails.keys())
        invalid_interfaces = set()

        for interface in interfaces:
            # The interface must match the regexes of atleast one area to pass
            passes_regex_check = False

            for area in areas:
                incl_regexes = area.include_interface_regexes
                excl_regexes = area.exclude_interface_regexes
                redistr_regexes = area.redistribute_interface_regexes

                passes_incl_regexes = self.validate_regexes(
                    incl_regexes, [interface], True  # expect at least one regex match
                )
                passes_excl_regexes = self.validate_regexes(
                    excl_regexes, [interface], False  # expect no regex match
                )
                passes_redistr_regexes = self.validate_regexes(
                    redistr_regexes, [interface], True
                )

                if (
                    passes_incl_regexes or passes_redistr_regexes
                ) and passes_excl_regexes:
                    passes_regex_check = True
                    break

            if not passes_regex_check:
                invalid_interfaces.add(interface)

        invalid_interface_dict = {
            interface: links.interfaceDetails[interface]
            for interface in invalid_interfaces
        }

        return invalid_interface_dict

    def _print_interface_validation_info(
        self,
        invalid_interfaces: Dict[str, Any],
    ) -> None:

        click.echo(
            self.validation_result_str(
                "link monitor", "Interface Regex Check", (len(invalid_interfaces) == 0)
            )
        )

        if len(invalid_interfaces) > 0:
            click.echo("Information about interfaces failing the regex check")
            self.print_links_table(invalid_interfaces)
