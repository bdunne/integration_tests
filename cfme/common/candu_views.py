from widgetastic_manageiq import LineChart
from widgetastic.widget import ConditionalSwitchableView, Text, TextInput, View
from widgetastic_patternfly import BootstrapSelect


class OptionForm(View):
    interval = BootstrapSelect(id='perf_typ')
    compare_to = BootstrapSelect(id='compare_to')
    show_weeks_back = BootstrapSelect(id='perf_days')
    show_mints_back = BootstrapSelect(id='perf_minutes')
    range = Text("//div[label[contains(.,'Range')]]//p")
    time_profile = Text("//div[label[contains(.,'Time Profile')]]//p")
    calendar = TextInput(locator=".//input[@id='miq_date_1']")


class VMUtilizationView(View):
    """A base view for VM Utilization"""
    title = Text(".//div[@id='main-content']//h1")
    options = View.nested(OptionForm)

    vm_cpu = LineChart(id='miq_chart_parent_candu_0')
    vm_cpu_state = LineChart(id='miq_chart_parent_candu_1')
    vm_memory = LineChart(id='miq_chart_parent_candu_2')
    vm_disk = LineChart(id='miq_chart_parent_candu_3')
    vm_network = LineChart(id='miq_chart_parent_candu_4')


class VMUtilizationAllView(VMUtilizationView):
    """A All view without select compare to option"""

    @property
    def is_displayed(self):
        if self.options.compare_to.is_displayed:
            return (
                "Capacity & Utilization data for Virtual Machine" in self.title.text and
                self.options.compare_to.selected_option == "<Nothing>"
            )
        else:
            return "Capacity & Utilization data for Virtual Machine" in self.title.text


class HostInfraUtilizationView(View):
    """View for Infrastructure provider Host Utilization"""
    title = Text(".//div[@id='main-content']//h1")
    options = View.nested(OptionForm)
    interval_type = ConditionalSwitchableView(reference='options.interval')

    @interval_type.register('Daily', default=True)
    class HostInfraDailyUtilizationView(View):
        """A view for Daily Interval Host Utilization"""
        host_cpu = LineChart(id='miq_chart_parent_candu_0')
        host_cpu_vm_avg = LineChart(id='miq_chart_candu_0_2')
        host_cpu_state = LineChart(id='miq_chart_parent_candu_1')
        host_cpu_state_vm_avg = LineChart(id='miq_chart_candu_1_2')
        host_memory = LineChart(id='miq_chart_parent_candu_2')
        host_memory_vm_avg = LineChart(id='miq_chart_candu_2_2')
        host_disk = LineChart(id='miq_chart_parent_candu_3')
        host_disk_vm_avg = LineChart(id='miq_chart_candu_3_2')
        host_network = LineChart(id='miq_chart_parent_candu_4')
        host_network_vm_avg = LineChart(id='miq_chart_candu_4_2')
        host_vm = LineChart(id='miq_chart_parent_candu_5')

    @interval_type.register('Hourly')
    class HostInfraHourlyUtilizationView(View):
        """A view for Hourly Interval Host Utilization"""
        host_cpu = LineChart(id='miq_chart_parent_candu_0')
        host_cpu_vm_avg = LineChart(id='miq_chart_candu_0_2')
        host_cpu_state = LineChart(id='miq_chart_parent_candu_1')
        host_cpu_state_vm_avg = LineChart(id='miq_chart_candu_1_2')
        host_memory = LineChart(id='miq_chart_parent_candu_2')
        host_memory_vm_avg = LineChart(id='miq_chart_candu_2_2')
        host_disk = LineChart(id='miq_chart_parent_candu_3')
        host_disk_vm_avg = LineChart(id='miq_chart_candu_3_2')
        host_network = LineChart(id='miq_chart_parent_candu_4')
        host_network_vm_avg = LineChart(id='miq_chart_candu_4_2')
        host_vm = LineChart(id='miq_chart_parent_candu_5')

    @interval_type.register('Most Recent Hour')
    class HostInfraRecentHourUtilizationView(View):
        """A view for Most Recent Hour Interval Host Utilization"""
        host_cpu = LineChart(id='miq_chart_parent_candu_0')
        host_memory = LineChart(id='miq_chart_parent_candu_2')
        host_disk = LineChart(id='miq_chart_parent_candu_3')
        host_network = LineChart(id='miq_chart_parent_candu_4')

    @property
    def is_displayed(self):
        expected_title = "{} Capacity & Utilization".format(self.context['object'].name)
        return self.title.text == expected_title
