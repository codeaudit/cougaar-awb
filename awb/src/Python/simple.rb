Cougaar::Model::Society.new('TINY-1AD-TRANS-STUB') do |society|
  society.add_host('ad') do |host|
    host.add_node('1AD_TINY') do |node|
      node.classname = 'org.cougaar.bootstrap.Bootstrapper'
      node.add_parameter('-Dorg.cougaar.node.name=1AD_TINY')
      node.add_parameter('-Dorg.cougaar.configuration.database=jdbc:mysql://ad/cougaar')
      node.add_parameter('-Dorg.cougaar.configuration.password=s0c0nfig')
      node.add_parameter('-Dorg.cougaar.configuration.user=society_config')
      node.add_parameter('-Dorg.cougaar.control.port=8484')
      node.add_parameter('-Dorg.cougaar.core.agent.startTime=08/10/2005')
      node.add_parameter('-Dorg.cougaar.core.persistence.clear=true')
      node.add_parameter('-Dorg.cougaar.core.persistence.enable=false')
      node.add_parameter('-Dorg.cougaar.experiment.id=EXPT-0001.TRIAL')
      node.add_parameter('-Dorg.cougaar.name.server=ad:8888:5555')
      node.add_parameter('-Dorg.cougaar.planning.ldm.lps.ComplainingLP.level=0')
      node.add_parameter('-Dorg.cougaar.tools.server.swallowOutputConnectionException=true')
      node.add_parameter('-Duser.timezone=GMT')
      node.add_prog_parameter('org.cougaar.core.node.Node')
      node.add_env_parameter('DISPLAY=AD:0.0')
      node.agent.add_component('1AD_TINY|org.cougaar.core.mobility.service.RootMobilityPlugin') do |c|
        c.classname = 'org.cougaar.core.mobility.service.RootMobilityPlugin'
        c.priority = 'COMPONENT'
        c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
      end
      node.add_agent('1-35-ARBN') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('1-35-ARBN|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('1-35-ARBN|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('1-35-ARBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('1-35-ARBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('1-35-ARBN|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('1-35-ARBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('1-35-ARBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('1-35-ARBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('1-35-ARBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('1-35-ARBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('1-35-ARBN|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-35-ARBN|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-35-ARBN|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-35-ARBN|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.demand.projection.LogClassIConsumerLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogClassIConsumerLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('subsistence.q')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.demand.projection.LogClassILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogClassILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('subsistence.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('1-35-ARBN|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('1-35-ARBN|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-35-ARBN|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-35-ARBN|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('Ammunition')
          c.add_argument('BulkPOL')
          c.add_argument('ClassISubsistence')
          c.add_argument('Consumable')
          c.add_argument('MaintainInventory')
          c.add_argument('PackagedPOL')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('1-35-ARBN|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-35-ARBN|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-35-ARBN|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('1-35-ARBN|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('1-35-ARBN|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('1-35-ARBN|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('1-35-ARBN|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('1-35-ARBN|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('1-6-INFBN') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('1-6-INFBN|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('1-6-INFBN|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('1-6-INFBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('1-6-INFBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('1-6-INFBN|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('1-6-INFBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('1-6-INFBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('1-6-INFBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('1-6-INFBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('1-6-INFBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('1-6-INFBN|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-6-INFBN|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-6-INFBN|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-6-INFBN|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.demand.projection.LogClassIConsumerLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogClassIConsumerLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('subsistence.q')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.demand.projection.LogClassILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogClassILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('subsistence.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('1-6-INFBN|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('1-6-INFBN|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-6-INFBN|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-6-INFBN|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('Ammunition')
          c.add_argument('BulkPOL')
          c.add_argument('ClassISubsistence')
          c.add_argument('Consumable')
          c.add_argument('MaintainInventory')
          c.add_argument('PackagedPOL')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('1-6-INFBN|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-6-INFBN|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-6-INFBN|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('1-6-INFBN|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('1-6-INFBN|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-INFBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('1-6-INFBN|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('1-6-INFBN|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('1-6-INFBN|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('1-AD') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('1-AD|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('1-AD|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('1-AD|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('1-AD|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('1-AD|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-AD|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-AD|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-AD|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-AD|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-AD|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('1-AD|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('1-AD|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-AD|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-AD|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-AD|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-AD|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('1-AD|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('1-AD|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('1AD_allocation_rules.xml')
        end
        agent.add_component('1-AD|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('1-AD|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('1-AD|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('1-AD|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('102-POL-SUPPLYCO') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-CORPS-POL-SUPPLYCO.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('102-POL-SUPPLYCO|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('106-TCBN') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('106-TCBN|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('106-TCBN|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('106-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('106-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('106-TCBN|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('106-TCBN|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('106-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('106-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('106-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('106-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('106-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('106-TCBN|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('106-TCBN|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('106-TCBN|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('106-TCBN|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('106-TCBN|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('106-TCBN|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('106-TCBN|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('106-TCBN|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('106-TCBN|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('106-TCBN|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('106-TCBN|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('106-TCBN|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('106-TCBN|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('106-TCBN|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('106-TCBN|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('106-TCBN|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('106-TCBN|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('106-TCBN|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('110-POL-SUPPLYCO') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-THEATER-POL-SUPPLYCO.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('110-POL-SUPPLYCO|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('123-MSB') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('123-MSB|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('123-MSB|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('123-MSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('123-MSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('123-MSB|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('123-MSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('123-MSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('123-MSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('123-MSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('123-MSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('123-MSB|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('123-MSB|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('123-MSB|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('123-MSB|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('123-MSB|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('123-MSB|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('123-MSB|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('123-MSB|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('Ammunition')
          c.add_argument('BulkPOL')
          c.add_argument('Consumable')
          c.add_argument('MaintainInventory')
          c.add_argument('PackagedPOL')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('123-MSB|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('123-MSB|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('123-MSB|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('123-MSB|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.inventory.InventoryPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.inventory.InventoryPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('123-MSB|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-MSB.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('123-MSB|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('123-MSB|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('123-MSB|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('16-CSG') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('16-CSG|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('16-CSG|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('16-CSG|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('16-CSG|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('16-CSG|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('16-CSG|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('16-CSG|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('16-CSG|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('16-CSG|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('16-CSG|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('16-CSG|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('16-CSG|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('16-CSG|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('16-CSG|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('16-CSG|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('16-CSG|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('16-CSG|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('16-CSG|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('16-CSG|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('16-CSG|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('16-CSG|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('16-CSG|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('16-CSG|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('16-CSG|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('16-CSG|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('16-CSG|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('16-CSG|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('16-CSG|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('16-CSG|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('18-MAINTBN') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('18-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('18-MAINTBN|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('18-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('18-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('18-MAINTBN|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('18-MAINTBN|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('18-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('18-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('18-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('18-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('18-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('18-MAINTBN|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('18-MAINTBN|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('18-MAINTBN|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('18-MAINTBN|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('18-MAINTBN|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('18-MAINTBN|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('18-MAINTBN|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('18-MAINTBN|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('18-MAINTBN|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('18-MAINTBN|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('18-MAINTBN|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('18-MAINTBN|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('18-MAINTBN|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('18-MAINTBN|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('18-MAINTBN|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('18-MAINTBN|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('18-MAINTBN|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('18-MAINTBN|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('191-ORDBN') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('191-ORDBN|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('191-ORDBN|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('191-ORDBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('191-ORDBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('191-ORDBN|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('191-ORDBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('191-ORDBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('191-ORDBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('191-ORDBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('191-ORDBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('191-ORDBN|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('191-ORDBN|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('191-ORDBN|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('191-ORDBN|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('191-ORDBN|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('191-ORDBN|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('191-ORDBN|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('191-ORDBN|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('191-ORDBN|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('191-ORDBN|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('191-ORDBN|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('191-ORDBN|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('191-ORDBN|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-THEATER-ORD-MGR.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('191-ORDBN|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('191-ORDBN|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('191-ORDBN|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('2-BDE-1-AD') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('2-BDE-1-AD|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('Ammunition')
          c.add_argument('BulkPOL')
          c.add_argument('Consumable')
          c.add_argument('MaintainInventory')
          c.add_argument('PackagedPOL')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('2-BDE-1-AD|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('21-TSC-HQ') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('21-TSC-HQ|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('21-TSC-HQ|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('21-TSC-HQ|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('21-TSC-HQ|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('21-TSC-HQ|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('21-TSC-HQ|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('21-TSC-HQ|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('21-TSC-HQ|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('21-TSC-HQ|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('21-TSC-HQ|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('21-TSC-HQ|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('227-SUPPLYCO') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('227-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-CORPS-SUPPLYCO.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('227-SUPPLYCO|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('28-TCBN') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('28-TCBN|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('28-TCBN|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('28-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('28-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('28-TCBN|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('28-TCBN|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('28-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('28-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('28-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('28-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('28-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('28-TCBN|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('28-TCBN|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('28-TCBN|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('28-TCBN|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('28-TCBN|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('28-TCBN|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('28-TCBN|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('28-TCBN|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('28-TCBN|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('28-TCBN|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('28-TCBN|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('28-TCBN|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('28-TCBN|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('28-TCBN|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('28-TCBN|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('28-TCBN|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('28-TCBN|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('28-TCBN|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('29-SPTGP') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('29-SPTGP|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('29-SPTGP|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('29-SPTGP|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('29-SPTGP|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('29-SPTGP|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('29-SPTGP|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('29-SPTGP|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('29-SPTGP|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('29-SPTGP|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('29-SPTGP|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('29-SPTGP|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('29-SPTGP|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('29-SPTGP|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('29-SPTGP|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('29-SPTGP|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('29-SPTGP|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('29-SPTGP|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('29-SPTGP|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('29-SPTGP|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('29-SPTGP|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('29-SPTGP|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('29-SPTGP|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('29-SPTGP|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('29-SPTGP|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('29-SPTGP|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('29-SPTGP|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('29-SPTGP|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('29-SPTGP|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('29-SPTGP|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('3-SUPCOM-HQ') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('3-SUPCOM-HQ|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('3-SUPCOM-HQ|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('343-SUPPLYCO') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('343-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-THEATER-SUPPLYCO.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('343-SUPPLYCO|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('37-TRANSGP') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('37-TRANSGP|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('37-TRANSGP|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('37-TRANSGP|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('37-TRANSGP|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('37-TRANSGP|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('37-TRANSGP|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('37-TRANSGP|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('37-TRANSGP|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('37-TRANSGP|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('37-TRANSGP|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('37-TRANSGP|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('37-TRANSGP|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('37-TRANSGP|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('37-TRANSGP|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('37-TRANSGP|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('37-TRANSGP|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('37-TRANSGP|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('37-TRANSGP|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('37-TRANSGP|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('37-TRANSGP|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('37-TRANSGP|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('37-TRANSGP|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('37-TRANSGP|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('37-TRANSGP|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('37-TRANSGP|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('37-TRANSGP|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('37-TRANSGP|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('37-TRANSGP|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('37-TRANSGP|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('47-FSB') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('47-FSB|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('47-FSB|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('47-FSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('47-FSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('47-FSB|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('47-FSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('47-FSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('47-FSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('47-FSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('47-FSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('47-FSB|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('47-FSB|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('47-FSB|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('47-FSB|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('47-FSB|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('47-FSB|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('47-FSB|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('47-FSB|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('Ammunition')
          c.add_argument('BulkPOL')
          c.add_argument('Consumable')
          c.add_argument('MaintainInventory')
          c.add_argument('PackagedPOL')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('47-FSB|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('47-FSB|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('47-FSB|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('47-FSB|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.inventory.InventoryPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.inventory.InventoryPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('47-FSB|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-FSB.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('47-FSB|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('47-FSB|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('47-FSB|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('485-CSB') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('485-CSB|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('485-CSB|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('485-CSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('485-CSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('485-CSB|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('485-CSB|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('485-CSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('485-CSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('485-CSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('485-CSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('485-CSB|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('485-CSB|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('485-CSB|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('485-CSB|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('485-CSB|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('485-CSB|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('485-CSB|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('485-CSB|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('485-CSB|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('485-CSB|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('485-CSB|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('485-CSB|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('485-CSB|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('485-CSB|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('485-CSB|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('485-CSB|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('485-CSB|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('485-CSB|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('485-CSB|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('5-CORPS') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('5-CORPS|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('5-CORPS|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('5-CORPS|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('5-CORPS|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('5-CORPS|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('5-CORPS|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('5-CORPS|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('5-CORPS|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('5-CORPS|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('5-CORPS|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('5-CORPS|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('5-CORPS|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('5-CORPS|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('5-CORPS|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('5-CORPS|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('5-CORPS|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('5-CORPS|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('5-CORPS|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('5-CORPS|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('5-CORPS|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('5-CORPS|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('5-CORPS|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('5-CORPS|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('51-MAINTBN') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('51-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('51-MAINTBN|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('51-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('51-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('51-MAINTBN|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('51-MAINTBN|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('51-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('51-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('51-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('51-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('51-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('51-MAINTBN|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('51-MAINTBN|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('51-MAINTBN|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('51-MAINTBN|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('51-MAINTBN|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('51-MAINTBN|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('51-MAINTBN|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('51-MAINTBN|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('51-MAINTBN|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('51-MAINTBN|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('51-MAINTBN|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('51-MAINTBN|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('51-MAINTBN|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('51-MAINTBN|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('51-MAINTBN|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('51-MAINTBN|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('51-MAINTBN|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('51-MAINTBN|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('565-RPRPTCO') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('565-RPRPTCO|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('565-RPRPTCO|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('565-RPRPTCO|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('565-RPRPTCO|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('565-RPRPTCO|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('565-RPRPTCO|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('565-RPRPTCO|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('565-RPRPTCO|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('565-RPRPTCO|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-CORPS-RPRPTCO.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('565-RPRPTCO|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('592-ORDCO') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('592-ORDCO|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('592-ORDCO|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('592-ORDCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('592-ORDCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('592-ORDCO|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('592-ORDCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('592-ORDCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('592-ORDCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('592-ORDCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('592-ORDCO|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('592-ORDCO|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('592-ORDCO|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('592-ORDCO|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('592-ORDCO|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('592-ORDCO|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('592-ORDCO|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('592-ORDCO|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('592-ORDCO|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('592-ORDCO|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('592-ORDCO|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('592-ORDCO|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('592-ORDCO|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogProjectionPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.execution.LogSupplyPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Ammunition') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Ammunition')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|BulkPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=BulkPOL')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|PackagedPOL') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=PackagedPOL')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Consumable') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Consumable')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.LogisticsOPlanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.inventory.InventoryPlugin|Subsistence') do |c|
          c.classname = 'org.cougaar.logistics.plugin.inventory.InventoryPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('SUPPLY_TYPE=Subsistence')
        end
        agent.add_component('592-ORDCO|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-CORPS-ORD-MGR.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('592-ORDCO|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('592-ORDCO|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('592-ORDCO|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('6-TCBN') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('6-TCBN|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('6-TCBN|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('6-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('6-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('6-TCBN|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('6-TCBN|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('6-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('6-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('6-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('6-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('6-TCBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('6-TCBN|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('6-TCBN|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('6-TCBN|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('6-TCBN|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('6-TCBN|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('6-TCBN|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('6-TCBN|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('6-TCBN|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('6-TCBN|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('6-TCBN|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('6-TCBN|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('6-TCBN|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('6-TCBN|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('6-TCBN|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('6-TCBN|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('6-TCBN|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('6-TCBN|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('6-TCBN|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('7-CSG') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('7-CSG|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('7-CSG|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('7-CSG|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('7-CSG|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('7-CSG|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('7-CSG|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('7-CSG|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('7-CSG|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('7-CSG|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('7-CSG|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('7-CSG|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('7-CSG|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('7-CSG|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('7-CSG|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('7-CSG|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('7-CSG|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('7-CSG|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('7-CSG|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('7-CSG|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('7-CSG|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('7-CSG|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('7-CSG|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('7-CSG|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('7-CSG|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('7-CSG|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('7-CSG|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('7-CSG|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('7-CSG|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('7-CSG|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('71-MAINTBN') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('71-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('71-MAINTBN|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('71-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('71-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('71-MAINTBN|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('71-MAINTBN|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('71-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('71-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('71-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('71-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('71-MAINTBN|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('71-MAINTBN|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('71-MAINTBN|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('71-MAINTBN|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('71-MAINTBN|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('71-MAINTBN|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('71-MAINTBN|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('71-MAINTBN|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('71-MAINTBN|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('71-MAINTBN|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('71-MAINTBN|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('MaintainInventory')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('71-MAINTBN|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('71-MAINTBN|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('71-MAINTBN|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('71-MAINTBN|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('71-MAINTBN|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('71-MAINTBN|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('71-MAINTBN|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('71-MAINTBN|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('AWR-2') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('AWR-2|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('AWR-2|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('AWR-2|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('AWR-2|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('AWR-2|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('AWR-2|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('AWR-2|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('AWR-2|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('AWR-2|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('AWR-2|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('AWR-2|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('AWR-2|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('AWR-2|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('AWR-2|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('AWR-2|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('AWR-2|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('AWR-2|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('AWR-2|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('AWR-2|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('AWR-2|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('AWR-2|org.cougaar.mlm.plugin.sample.UniversalAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.UniversalAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('ProjectSupply')
          c.add_argument('Supply')
        end
        agent.add_component('AWR-2|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('AWR-2|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('AWR-2|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('DISCOM-1-AD') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('DISCOM-1-AD|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogMEILDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisMEI.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.demand.projection.LogPartsLDMPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('icisParts.q')
          c.add_argument('+PrototypeProvider')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('Ammunition')
          c.add_argument('BulkPOL')
          c.add_argument('Consumable')
          c.add_argument('MaintainInventory')
          c.add_argument('PackagedPOL')
          c.add_argument('StrategicTransportation')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.StrategicTransportProjectorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('OriginFile=None')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('default_allocation_rules.xml')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=InventoryPolicy-ARBN.ldm.xml')
          c.add_argument('DESTINATION=none')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.mlm.plugin.ldm.LDMSQLPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.LDMSQLPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('fdm_equip.q')
        end
        agent.add_component('DISCOM-1-AD|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('DLAHQ') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('DLAHQ|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('DLAHQ|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('DLAHQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('DLAHQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('DLAHQ|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('DLAHQ|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('DLAHQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('DLAHQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('DLAHQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('DLAHQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('DLAHQ|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('DLAHQ|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DLAHQ|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DLAHQ|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DLAHQ|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DLAHQ|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DLAHQ|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DLAHQ|org.cougaar.mlm.plugin.sample.UniversalAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.UniversalAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('ProjectSupply')
          c.add_argument('Supply')
        end
        agent.add_component('DLAHQ|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('DLAHQ|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('DLAHQ|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('HNS') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('HNS|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('HNS|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('HNS|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('HNS|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('HNS|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('HNS|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('HNS|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('HNS|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('HNS|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('HNS|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('HNS|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('HNS|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('HNS|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('HNS|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('HNS|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('HNS|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('HNS|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('HNS|org.cougaar.mlm.plugin.sample.UniversalAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.UniversalAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('ProjectSupply')
          c.add_argument('Supply')
        end
        agent.add_component('HNS|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('HNS|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('HNS|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('NCA') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('NCA|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('NCA|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('NCA|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('NCA|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('NCA|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('NCA|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('NCA|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('NCA|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('NCA|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('NCA|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('NCA|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('NCA|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('NCA|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('NCA|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('NCA|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('NCA|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('NCA|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('NCA|org.cougaar.mlm.plugin.organization.GLSInitServlet') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSInitServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('093FF.oplan.q')
        end
        agent.add_component('NCA|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('NCA|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('NCA|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('NCA|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('NCA|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('OSC') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('OSC|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('OSC|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('OSC|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('OSC|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('OSC|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('OSC|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('OSC|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('OSC|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('OSC|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('OSC|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('OSC|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('OSC|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('OSC|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('OSC|OSCAmmoPacker|org.cougaar.logistics.plugin.trans.AmmoLowFidelityExpanderPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.trans.AmmoLowFidelityExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('OSC|OSCAmmoPacker|org.cougaar.logistics.plugin.packer.ALAmmoPacker') do |c|
          c.classname = 'org.cougaar.logistics.plugin.packer.ALAmmoPacker'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('OSC|OSCAmmoPacker|org.cougaar.logistics.plugin.trans.AmmoProjectionExpanderPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.trans.AmmoProjectionExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('OSC|OSCAmmoPacker|org.cougaar.mlm.plugin.generic.GenericTablePlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.GenericTablePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('IOC_allocation_rules.xml')
        end
        agent.add_component('OSC|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('OSC|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('OSC|org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.xml.XMLPrototypeProviderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('OSC|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('OSC|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('OSC|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('OSC|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('OSC|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('TRANSCOM') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('TRANSCOM|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('TRANSCOM|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('TRANSCOM|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('TRANSCOM|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('TRANSCOM|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('TRANSCOM|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('TRANSCOM|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('TRANSCOM|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('TRANSCOM|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('TRANSCOM|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('TRANSCOM|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('TRANSCOM|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('TRANSCOM|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('TRANSCOM|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('TRANSCOM|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('TRANSCOM|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('TRANSCOM|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('TRANSCOM|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('TRANSCOM|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('TRANSCOM|org.cougaar.mlm.plugin.sample.UniversalAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.sample.UniversalAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('Transport')
        end
        agent.add_component('TRANSCOM|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('USAEUR') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('USAEUR|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('USAEUR|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('USAEUR|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('USAEUR|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('USAEUR|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('USAEUR|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('USAEUR|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('USAEUR|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('USAEUR|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('USAEUR|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('USAEUR|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('USAEUR|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USAEUR|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USAEUR|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USAEUR|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USAEUR|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USAEUR|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USAEUR|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USAEUR|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USAEUR|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USAEUR|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('POLICY=ArmyFeedingPolicy.ldm.xml')
          c.add_argument('DESTINATION=Subordinate')
          c.add_argument('POLICY=LimitResourcesPolicy.ldm.xml')
          c.add_argument('DESTINATION=Subordinate')
        end
        agent.add_component('USAEUR|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('USAEUR|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
      node.add_agent('USEUCOM') do |agent|
        agent.classname = 'org.cougaar.core.agent.SimpleAgent'
        agent.add_component('USEUCOM|org.cougaar.core.servlet.SimpleServletComponent') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.PlanViewServlet')
          c.add_argument('/tasks')
        end
        agent.add_component('USEUCOM|org.cougaar.glm.servlet.GLMCompletionServlet') do |c|
          c.classname = 'org.cougaar.glm.servlet.GLMCompletionServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/completion')
        end
        agent.add_component('USEUCOM|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.planning.servlet.HierarchyServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.planning.servlet.HierarchyServlet')
          c.add_argument('/hierarchy')
        end
        agent.add_component('USEUCOM|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.mlm.ui.servlet.DataGathererServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.mlm.ui.servlet.DataGathererServlet')
          c.add_argument('/datagatherer')
        end
        agent.add_component('USEUCOM|org.cougaar.logistics.servlet.LogisticsInventoryServletComponent') do |c|
          c.classname = 'org.cougaar.logistics.servlet.LogisticsInventoryServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.logistics.servlet.LogisticsInventoryServlet')
          c.add_argument('/log_inventory')
        end
        agent.add_component('USEUCOM|org.cougaar.planning.servlet.LoaderServletComponent') do |c|
          c.classname = 'org.cougaar.planning.servlet.LoaderServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('/load')
        end
        agent.add_component('USEUCOM|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.AgentInfoServlet')
          c.add_argument('/CSMART_AgentInfoServlet')
        end
        agent.add_component('USEUCOM|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.CommunityProviderServlet')
          c.add_argument('/CSMART_CommunityProviderServlet')
        end
        agent.add_component('USEUCOM|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.MetricsServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.MetricsServlet')
          c.add_argument('/CSMART_MetricsServlet')
        end
        agent.add_component('USEUCOM|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.SearchServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.SearchServlet')
          c.add_argument('/CSMART_SearchServlet')
        end
        agent.add_component('USEUCOM|org.cougaar.core.servlet.SimpleServletComponent|org.cougaar.tools.csmart.ui.servlet.PlanServlet') do |c|
          c.classname = 'org.cougaar.core.servlet.SimpleServletComponent'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('org.cougaar.tools.csmart.ui.servlet.PlanServlet')
          c.add_argument('/CSMART_PlanServlet')
        end
        agent.add_component('USEUCOM|org.cougaar.core.topology.TopologyReaderServlet') do |c|
          c.classname = 'org.cougaar.core.topology.TopologyReaderServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USEUCOM|org.cougaar.core.mobility.servlet.MoveAgentServlet') do |c|
          c.classname = 'org.cougaar.core.mobility.servlet.MoveAgentServlet'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USEUCOM|org.cougaar.core.mobility.service.RedirectMovePlugin') do |c|
          c.classname = 'org.cougaar.core.mobility.service.RedirectMovePlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USEUCOM|org.cougaar.community.CommunityPlugin') do |c|
          c.classname = 'org.cougaar.community.CommunityPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USEUCOM|org.cougaar.mlm.plugin.organization.OrgDataPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgDataPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USEUCOM|org.cougaar.mlm.plugin.organization.OrgReportPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.OrgReportPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USEUCOM|org.cougaar.mlm.plugin.organization.GLSExpanderPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSExpanderPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USEUCOM|org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.organization.GLSAllocatorPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USEUCOM|org.cougaar.mlm.plugin.ldm.GetOplanPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.ldm.GetOplanPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USEUCOM|org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin') do |c|
          c.classname = 'org.cougaar.logistics.plugin.policy.LogisticsPolicyManagerPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
        end
        agent.add_component('USEUCOM|org.cougaar.mlm.plugin.generic.PropagationPlugin') do |c|
          c.classname = 'org.cougaar.mlm.plugin.generic.PropagationPlugin'
          c.priority = 'COMPONENT'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin'
          c.add_argument('forward.xml')
        end
        agent.add_component('USEUCOM|org.cougaar.core.examples.DummyBinder') do |c|
          c.classname = 'org.cougaar.core.examples.DummyBinder'
          c.priority = 'BINDER'
          c.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Binder'
        end
      end
    end
  end
end
