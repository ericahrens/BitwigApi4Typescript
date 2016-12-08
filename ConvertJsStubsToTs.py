from os import listdir
from os.path import isfile, join
from sys import platform

import re

"""
 Program that converts JavaScripts Stubs for Bitwig Studio Controller API into a
 Typescript Definition File.
"""
__author__ = "Eric Ahrens"
__version__ = "1.0.0"
__maintainer__ = "Eric Ahrens"
__email__ = "eric.n.ahrens@gmail.com"

if platform == "darwin":
    stubspath = "/Applications/Bitwig Studio.app/Contents/Resources/Documentation/control-surface/js-stubs"
elif platform == "win32":
    stubspath = "C:/Program Files (x86)/Bitwig Studio/resources/doc/control-surface/js-stubs"

result_filename = "BitwigControllerApi.d.ts"
with_comments = True
with_types = True

head = "declare function loadAPI(val: number): void;\n" \
       "declare function println(s : string) : void;\n" \
       "declare function load(file: string) : void;\n" \
       "declare var host : Host;\n\n" \
       "declare enum CursorNavigationMode  {\n" \
       "	NESTED = 0,\n" \
       "	FLAT,\n" \
       "	GUI,\n" \
       "}\n"

parameterPaths = {
    'MidiIn.createNoteInput./*': -1,
    'MidiIn.createNoteInput.*/masks': '...masks: string[]',
    'MidiIn.setMidiCallback.callback': 'callback : (status: number, data1: number, data2: number) => void',
    'Application.addHasActiveEngineObserver.callable': 'callable : (engineactive : boolean) => void',
    'Application.addProjectNameObserver.callback': 'callback : (name : string) => void',
    'Application.addPanelLayoutObserver.callable': 'callable : (layoutName : string) => void',
    'Application.addDisplayProfileObserver.callable': 'callable : (profileName : string) => void',
    'AutomatableRangedValue.addNameObserver.callback': 'callback : (name : string) => void',
    'AutomatableRangedValue.addValueDisplayObserver.callback': 'callback : (displayValue : string) => void',
    'BeatTime.addTimeObserver.callback': 'callback : (timeFloat : number) => void',
    'BeatTime.addRawValueObserver.callback': 'callback : (floatValue : number) => void',
    'Browser.addIsBrowsingObserver.callback': 'callback : (isbrowsing : boolean) => void',
    'BrowserColumn.addExistsObserver.callback': 'callback : (exists : boolean ) => void',
    'BrowserColumn.addEntryCountObserver.callback': 'callback : (count: number ) => void',
    'BrowserFilterColumn.addNameObserver.callback': 'callback : (name: string ) => void',
    'BrowserFilterColumnBank.addScrollPositionObserver.callback': 'callback : (position: number) => void',
    'BrowserFilterColumnBank.addCanScrollUpObserver.callback': 'callback : (canscroll: boolean) => void',
    'BrowserFilterColumnBank.addCanScrollDownObserver.callback': 'callback : (canscroll: boolean) => void',
    'BrowserFilterColumnBank.addEntryCountObserver.callback': 'callback : (count: number) => void',
    'BrowserFilterItem.addHitCountObserver.callback': 'callback : (count: number) => void',
    'BrowserItem.addExistsObserver.callback': 'callback : (exists: boolean ) => void',
    'BrowserItem.addValueObserver.callback': 'callback : (value: string) => void',
    'BrowserItemBank.addScrollPositionObserver.callback': 'callback : (position: number) => void',
    'BrowserItemBank.addCanScrollUpObserver.callback': 'callback : (canscroll: boolean) => void',
    'BrowserItemBank.addCanScrollDownObserver.callback': 'callback : (canscroll: boolean) => void',
    'BrowsingSession.addIsAvailableObserver.callback': 'callback : (available: boolean) => void',
    'BrowsingSession.addIsActiveObserver.callback': 'callback : (active: boolean ) => void',
    'BrowsingSession.addHitCountObserver.callback': 'callback : (hitcount: number ) => void',
    'BrowsingSessionBank.addScrollPositionObserver.callback': 'callback : (position: number) => void',
    'BrowsingSessionBank.addCanScrollUpObserver.callback': 'callback : (canscroll: boolean) => void',
    'BrowsingSessionBank.addCanScrollDownObserver.callback': 'callback : (canscroll: boolean) => void',
    'BrowsingSessionBank.addEntryCountObserver.callback': 'callback : (count: number ) => void',
    'Channel.addVuMeterObserver.callback': 'callback : (value : number) => void',
    'Channel.addNoteObserver.callback': 'callback : (onoff: boolean, key: number, velocity: number) => void',
    'Channel.addColorObserver.callback': 'callback : (red: number, green: number, blue: number) => void',
    'Channel.addIsSelectedInMixerObserver.callback': 'callback : (selected: boolean ) => void',
    'ChannelBank.addChannelScrollPositionObserver.callback': 'callback : (position: number ) => void',
    'ChannelBank.addCanScrollChannelsUpObserver.callback': 'callback : (canscroll: boolean ) => void',
    'ChannelBank.addCanScrollChannelsDownObserver.callback': 'callback : (canscroll: boolean ) => void',
    'ChannelBank.addChannelCountObserver.callback': 'callback : ( count: number) => void',
    'ChannelBank.addCanScrollSendsUpObserver.callback': 'callback : (canscroll: boolean ) => void',
    'ChannelBank.addCanScrollSendsDownObserver.callback': 'callback : (canscroll: boolean ) => void',
    'ChannelBank.addSendCountObserver.callback': 'callback : (count: number ) => void',
    'Clip.addCanScrollKeysUpObserver.callback': 'callback : (canscroll: boolean ) => void',
    'Clip.addCanScrollKeysDownObserver.callback': 'callback : (canscroll: boolean ) => void',
    'Clip.addCanScrollStepsBackwardsObserver.callback': 'callback : (canscroll: boolean ) => void',
    'Clip.addCanScrollStepsForwardObserver.callback': 'callback : (canscroll: boolean ) => void',
    'Clip.addStepDataObserver.callback': 'callback : (x: number, y: number, state: number ) => void',
    'Clip.addPlayingStepObserver.callback': 'callback : (steppos: number) => void',
    'Clip.addColorObserver.callback' : 'callback : (red: number, green: number, blue: number ) => void',
    'Scene.addClipCountObserver.callback' : 'callback : (count: number) => void',
    'ClipLauncherScenesOrSlots.addNameObserver.callback': 'callback : (name: string) => void',
    'ClipLauncherSlots.addIsSelectedObserver.callback': 'callback : (index: number, selected: boolean) => void',
    'ClipLauncherSlots.addHasContentObserver.callback': 'callback : (index: number, hasContent: boolean ) => void',
    'ClipLauncherSlots.addPlaybackStateObserver.callback': 'callback : (index: number, state: number, queued: boolean) => void',
    'ClipLauncherSlots.addIsPlayingObserver.callback': 'callback : (index: number, playing: boolean) => void',
    'ClipLauncherSlots.addIsRecordingObserver.callback': 'callback : (index: number, recording: boolean) => void',
    'ClipLauncherSlots.addIsPlaybackQueuedObserver.callback': 'callback : (index: number, playbackQueued: boolean) => void',
    'ClipLauncherSlots.addIsRecordingQueuedObserver.callback': 'callback : (index: number, recordingQueued: boolean) => void',
    'ClipLauncherSlots.addIsStopQueuedObserver.callback': 'callback : (index: number, stopQueued: boolean) => void',
    'ClipLauncherSlots.addColorObserver.callback': 'callback : (index: number, red: number, green: number, blue: number) => void',
    'Cursor.addCanSelectPreviousObserver.callback': 'callback : (canSelect: boolean) => void',
    'Cursor.addCanSelectNextObserver.callback': 'callback : (canSelect: boolean) => void',
    'Device.addPositionObserver.callback': 'callback : (position: number) => void',
    'Device.addHasSelectedDeviceObserver.callback': 'callback : (hasSelectedDevice: boolean) => void',
    'Device.addIsPluginObserver.callback': 'callback : (isPlugin: boolean) => void',
    'Device.addPreviousParameterPageEnabledObserver.callback': 'callback : (enabled: boolean) => void',
    'Device.addNextParameterPageEnabledObserver.callback': 'callback : (enabled: boolean) => void',
    'Device.addNameObserver.callback': 'callback : (name: string) => void',
    'Device.addPresetNameObserver.callback': 'callback : (name: string) => void',
    'Device.addPresetCategoryObserver.callback': 'callback : (category: string) => void',
    'Device.addPresetCreatorObserver.callback': 'callback : (name: string) => void',
    'Device.addSelectedPageObserver.callback': 'callback : (index: number) => void',
    'Device.addActiveModulationSourceObserver.callback': 'callback : (name: string) => void',
    'Device.addPageNamesObserver.callback': 'callback : (name: string) => void',
    'Device.addPresetNamesObserver.callback': 'callback : (names: string[]) => void',
    'Device.addPresetCategoriesObserver.callback': 'callback : (categories: string[]) => void',
    'Device.addPresetCreatorsObserver.callback': 'callback : (creators: string[]) => void',
    'Device.addIsEnabledObserver.callback': 'callback : (enabled: boolean) => void',
    'Device.addSlotsObserver.callback': 'callback : (slotnames: string[]) => void',
    'Device.addDirectParameterIdObserver.callback': 'callback : (parameterIds: string[]) => void',
    'Device.addDirectParameterNameObserver.callback': 'callback : (id: string, name: string) => void',
    'Device.addDirectParameterValueDisplayObserver.callback': 'callback : (id: string, valueDisplay: string) => void',
    'Device.addDirectParameterNormalizedValueObserver.callback': 'callback : (id: string, value: number) => void',
    'Device.addSampleNameObserver.callback': 'callback : (name: string) => void',
    'DeviceBank.addScrollPositionObserver.callback': 'callback : (position: number) => void',
    'DeviceBank.addCanScrollUpObserver.callback': 'callback : (canScroll: boolean) => void',
    'DeviceBank.addCanScrollDownObserver.callback': 'callback : (canScroll: boolean) => void',
    'DeviceBank.addDeviceCountObserver.callback': 'callback : (count: number) => void',
    'DeviceChain.addNameObserver.callback': 'callback : (name: string) => void',
    'DeviceChain.addIsSelectedInEditorObserver.callback': 'callback : (selected: boolean) => void',
    'GenericBrowsingSession.addNameObserver.callback': 'callback : (name: string) => void',
    'Host.scheduleTask.callback': 'callback : (connection: RemoteConnection ) => void',
    'Host.connectToRemoteHost.callback': 'callback : ( ) => void',
    'Host.addDatagramPacketObserver.callback': 'callback : (data) => void',
    'Macro.addLabelObserver.callback': 'callback : (name: string) => void',
    'MidiIn.setSysexCallback.callback': 'callback : (data: string) => void',
    'ModulationSource.addIsMappingObserver.callback': 'callback : (isMapping: boolean) => void',
    'ModulationSource.addNameObserver.callback': 'callback : (name: string) => void',
    'ModulationSource.addIsMappedObserver.callback': 'callback : (mapped: boolean) => void',
    'NoteLane.addNoteValueObserver.callback': 'callback : (value: number) => void',
    'NoteLane.addNameObserver.callback': 'callback : (name: string ) => void',
    'NoteLane.addColorObserver.callback': 'callback : (red: number, green: number, blue: number) => void',
    'PrimaryDevice.addCanSwitchToDeviceObserver.callback': 'callback : (canSwitch: boolean) => void',
    'RangedValue.addValueObserver.callback': 'callback : (value: number) => void',
    'RangedValue.addRawValueObserver.callback': 'callback : (value: number) => void',
    'RemoteConnection.setDisconnectCallback.callback': 'callback : ( ) => void',
    'RemoteConnection.setReceiveCallback.callback': 'callback : (data: number[]) => void',
    'RemoteSocket.setClientConnectCallback.callback': 'callback : (connection: RemoteConnection) => void',
    'Scene.addPositionObserver.callback': 'callback : (position: number) => void',
    'Scene.addIsSelectedInEditorObserver.callback': 'callback : (selected: boolean) => void',
    'SceneBank.addScrollPositionObserver.callback': 'callback : (position: number) => void',
    'SceneBank.addCanScrollUpObserver.callback': 'callback : (canScroll: boolean) => void',
    'SceneBank.addCanScrollDownObserver.callback': 'callback : (canScroll: boolean) => void',
    'SceneBank.addSceneCountObserver.callback': 'callback : (count: number) => void',
    'Signal.addSignalObserver.callback': 'callback : ( ) => void',
    'Track.addPositionObserver.callback': 'callback : (postion: number) => void',
    'Track.addIsQueuedForStopObserver.callback': 'callback : (queued: boolean) => void',
    'Track.addPitchNamesObserver.callback': 'callback : (key: number, name: string) => void',
    'Track.addTrackTypeObserver.callback': 'callback : (type: string) => void',
    'Track.addIsGroupObserver.callback': 'callback : (group: boolean) => void',
    'TrackBank.addSceneScrollPositionObserver.callback': 'callback : (position: number) => void',
    'TrackBank.addCanScrollScenesUpObserver.callback': 'callback : (canScroll: boolean) => void',
    'TrackBank.addCanScrollScenesDownObserver.callback': 'callback : (canScroll: boolean) => void',
    'TrackBank.addSceneCountObserver.callback': 'callback : (count: number) => void',
    'Transport.addIsPlayingObserver.callback': 'callback : (playing: boolean) => void',
    'Transport.addIsRecordingObserver.callback': 'callback : (recording: boolean) => void',
    'Transport.addOverdubObserver.callback': 'callback : (overdub: boolean) => void',
    'Transport.addLauncherOverdubObserver.callback': 'callback : (overdub: boolean) => void',
    'Transport.addAutomationWriteModeObserver.callback': 'callback : (mode: string) => void',
    'Transport.addIsWritingArrangerAutomationObserver.callback': 'callback : (writeEnabled: boolean) => void',
    'Transport.addIsWritingClipLauncherAutomationObserver.callback': 'callback : (writingClipLauncher: boolean) => void',
    'Transport.addAutomationOverrideObserver.callback': 'callback : (automationOverride: boolean) => void',
    'Transport.addIsLoopActiveObserver.callback': 'callback : (loopActive: boolean) => void',
    'Transport.addPunchInObserver.callback': 'callback : (enabled: boolean) => void',
    'Transport.addPunchOutObserver.callback': 'callback : (enabled: boolean ) => void',
    'Transport.addClickObserver.callback': 'callback : (active: boolean) => void',
    'Transport.addMetronomeTicksObserver.callback': 'callback : (active: boolean) => void',
    'Transport.addMetronomeVolumeObserver.callback': 'callback : (value: number) => void',
    'Transport.addPreRollClickObserver.callback': 'callback : (enabled: boolean) => void',
    'Transport.addPreRollObserver.callback': 'callback : (enabled: boolean) => void',
    'Transport.addClipLauncherPostRecordingActionObserver.callback': 'callback : (status: string) => void',
    'Value.addValueObserver.callback': 'callback : (value) => void',
}

functionPaths = {
    'BooleanValue.toggle': 'exclusive?'
}

filelist = [f for f in listdir(stubspath) if isfile(join(stubspath, f))]

resultfile = open(result_filename, 'w')

parsers = []


class Parameter:
    def __init__(self, name, comment=None):
        self.__name = name
        self.__type = comment.get_type(name)

    def overwrite(self, paramdisp):
        self.__name = paramdisp
        self.__type = None

    @property
    def name(self):
        return self.__name

    @property
    def type_str(self):
        return self.__type

    @property
    def type(self):
        if self.__type == 'function':
            return '() => void'
        if self.__type == 'byte[]':
            return 'number[]'
        if self.__type == 'int' or self.__type == 'double' or self.__type == 'long' or self.__type == 'byte':
            return 'number'
        return self.__type


class Method:
    def __init__(self, className, deflist, comment):
        self.__name = None
        self.__parameters = []
        self.__constructor = False
        self.__name = deflist[2]
        self.__returntype = comment.get_return_type()
        self.__lines = comment.get_comments()
        if self.__name == 'constructor':
            self.__constructor = True
            for idx in range(3, len(deflist)):
                self.__parameters.append(Parameter(deflist[idx], comment))
        else:
            for idx in range(4, len(deflist)):
                param = Parameter(deflist[idx], comment)
                qpath = className + "." + self.__name + "." + param.name
                if qpath in parameterPaths and with_types:
                    ref = parameterPaths[qpath]
                    if ref != -1:
                        param.overwrite(ref)
                        self.__parameters.append(param)
                else:
                    self.__parameters.append(param)
                    if param.type_str == 'function':
                        print ("    \'" + className + "." + self.__name + "." + param.name + "' : '" + param.name + " : ( ) => void',")

    def is_constructor(self):
        return self.__constructor

    def constr_param(self):
        if self.__constructor and len(self.__parameters) > 0:
            return self.__parameters[0].name
        return None

    def render(self, file, class_name):
        if not self.__constructor:
            if with_comments:
                for cl in self.__lines:
                    file.write("    " + cl + "\n")

            file.write("     " + self.__name + "(")
            q_path = class_name + "." + self.__name
            if q_path in functionPaths and with_types:
                file.write(functionPaths[q_path])
            else:
                for idx, parameter in enumerate(self.__parameters):
                    if parameter.type and with_types:
                        file.write(parameter.name + " : " + parameter.type)
                    else:
                        file.write(parameter.name)
                    if idx < len(self.__parameters) - 1:
                        file.write(", ")
            if with_types:
                if self.__returntype:
                    file.write(") : " + self.__returntype)
                else:
                    file.write(") : void")
            else:
                file.write(")")

class Comment:
    def __init__(self):
        self.__return_type = None
        self.__paramDict = {}
        self.__lines = []

    def set_return_type(self, type):
        self.__return_type = re.sub('[\{\}]', '', type)

    def get_return_type(self):
        if self.__return_type == 'function':
            return '() => void'
        if self.__return_type == 'byte[]':
            return 'number[]'
        if self.__return_type == 'int' or self.__return_type == 'double' or self.__return_type == 'long' or self.__return_type == 'byte':
            return 'number'
        return self.__return_type

    def register_type(self, type, paramname):
        self.__paramDict[paramname] = re.sub('[\{\}]', '', type)

    def get_type(self, param_name):
        if param_name in self.__paramDict:
            return self.__paramDict[param_name]
        return None

    def add_line(self, line):
        self.__lines.append(line)

    def get_comments(self):
        return [l for l in self.__lines]


class ClassParser:
    def __init__(self, lines, filename):
        self.__fileName = filename
        self.__methods = []
        self.__className = None
        self.__super = None
        self.__class_comment = []
        funcdef = None
        constrdef = None

        in_comment_mode = False
        current_comment = None

        for line in lines:
            sline = line.strip()
            if sline.startswith('/**'):
                in_comment_mode = True
                current_comment = Comment()
                current_comment.add_line(sline)
            elif sline.startswith('*/'):
                current_comment.add_line(sline)
                in_comment_mode = False
            elif in_comment_mode:
                current_comment.add_line(sline)
                lineArray = [s for s in re.split(" |\.|\*|=|,|\(|\)|;|\n", sline) if len(s.strip()) > 0]
                if len(lineArray) > 2:
                    anotation = lineArray[0]
                    if anotation.startswith('@return'):
                        current_comment.set_return_type(lineArray[1])
                    elif anotation.startswith('@param'):
                        current_comment.register_type(lineArray[1], lineArray[2])
            if sline.startswith('var'):
                # print " ###### " + line
                pass
            elif sline.startswith('function'):
                # print line
                m = re.split('\W+', sline)
                if m and len(m) > 1:
                    self.__className = m[1]
                    funcdef = m[1] + '.prototype.'
                    constrdef = m[1] + '.prototype'
                    self.__class_comment = current_comment.get_comments()
                    # print "[" + self.__className + "]"
            elif self.__className and line.startswith(funcdef):
                lineArray = [s for s in re.split(" |\.|=|,|\(|\)|\{|\}|;|\n", sline) if len(s.strip()) > 0]
                if len(lineArray) > 3:
                    method = Method(self.__className, lineArray, current_comment)
                    if not method.is_constructor():
                        self.__methods.append(method)
                else:
                    print (" <<<<<<<<<<<<<<<<<<<< FAIL >>>>>>>>>>>>>>> ")
            elif constrdef and line.startswith(constrdef):
                lineArray = [s for s in re.split(" |\.|=|,|\(|\)|\{|\}|;|\n", sline) if len(s.strip()) > 0]
                if len(lineArray) > 3:
                    self.__super = lineArray[3]

    @property
    def name(self):
        return self.__className

    @property
    def filename(self):
        return self.__fileName

    def render(self, file):
        if not self.name:
            return
        if with_comments:
            for cl in self.__class_comment:
                file.write(cl + "\n")

        file.write('interface ' + p.name)
        if self.__super:
            file.write(' extends ' + self.__super)
        file.write(' {\n')
        for idx, method in enumerate(self.__methods):
            method.render(file, self.__className)
            if idx < len(self.__methods) - 1:
                file.write(",\n")
        if with_comments:
            file.write("\n")

        file.write('}\n\n')


def readFile(filename):
    # print " ###### Reading FILE: " + filename + " ############ "
    with open(stubspath + "/" + filename) as file:
        content = file.readlines()        # print " LINES = " + str(len(content))
        parsers.append(ClassParser(content, filename))


for f in filelist:
    readFile(f)

resultfile.write(head);
for p in parsers:
    p.render(resultfile)

resultfile.close()
print("Created Typescript definition File: " + result_filename)
