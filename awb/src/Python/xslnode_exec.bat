@ECHO OFF 
@REM Generated by XSLNode.bat! 
java.exe  -Djava.class.path=%COUGAAR_INSTALL_PATH%/lib/bootstrap.jar -Dorg.cougaar.config.path=%COUGAAR_INSTALL_PATH%/GameOfLife/configs\;$COUGAAR_INSTALL_PATH/configs/common -Dorg.cougaar.core.agent.quiet=true -Dorg.cougaar.core.agent.showtraffic=false -Dorg.cougaar.core.node.InitializationComponent=XML -Dorg.cougaar.install.path=%COUGAAR_INSTALL_PATH% -Dorg.cougaar.name.server=localhost:8888:5555 -Dorg.cougaar.node.name=GameNode -Dorg.cougaar.society.file=GameOfLife.xml -Dorg.cougaar.system.path=%COUGAAR_INSTALL_PATH%/sys -Dorg.cougaar.workspace=%COUGAAR_INSTALL_PATH%/workspace -Xbootclasspath/p:%COUGAAR_INSTALL_PATH%/lib/javaiopatch.jar -Xms16m -Xmx128m -XX:ThreadStackSize=256 org.cougaar.bootstrap.Bootstrapper org.cougaar.core.node.Node