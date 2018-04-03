import pandas as pd
import pprint
import os
import sys


class Synchronizer:
    def __init__(self):
        self.synchronizedTriggers = {"Time(s)":[],"Event":[]}
        self.keepedTriggers = {"LeftBoundary" : [],"RightBoundary":[],"Trigger":[],"Event" : []}
        self.rejectedTriggers = {}
        self.toDrop = []
    
    def synchronizeTriggersTime(self):
        deltaStartEnd = 0
        actualTime = 0
        for index,row in self.artifacts.iterrows():
            
            trigToKeep = self.triggers[(self.triggers['Time(s)'] >= row['Startkeep(s)']) & (self.triggers['Time(s)'] <= row['Endkeep(s)'])]
            b = {
                'left' : row['Startkeep(s)'],
                'right' : row['Endkeep(s)']
                }

            if not trigToKeep.empty: actualTime = self.testTrigger(actualTime,b, trigToKeep)
            else:
                # Calculating delta between Start and End of the row
                deltaStartEnd = row['Endkeep(s)'] - row['Startkeep(s)']
                actualTime+=deltaStartEnd

        self.rejectedTriggers = self.triggers.drop(self.toDrop)
    
    def importFiles(self,pathToTriggers,pathToArtifacts):
        if not os.path.exists(pathToTriggers):
            sys.exit('Trigger file does not exist')
        else:
            self.triggers = pd.read_excel(pathToTriggers)

        if not os.path.exists(pathToArtifacts):
            sys.exit('Artifacts file does not exist')
        else:
            self.artifacts = pd.read_excel(pathToArtifacts)
               
    def exportSynchronizedTriggers(self,path):
        writer = pd.ExcelWriter(path)
        pd.DataFrame(data=self.synchronizedTriggers).to_excel(writer, 'Triggers',index=False)
        pd.DataFrame(data=self.keepedTriggers).to_excel(writer, 'Keeped',index=False)
        pd.DataFrame(data=self.rejectedTriggers).to_excel(writer, 'Rejected',index=False)
        writer.save()
    
    def testTrigger(self,time,borne,trigs):
        left = borne['left']
        right = borne['right']
        prevTrig = "";
        lastIdx = trigs.index[-1]
        firstIdx = trigs.index[0]

        for index,t in trigs.iterrows():
            self.toDrop.append(index)
            if index == firstIdx:
                prevTrig = t
                time += t['Time(s)'] - left
                self.synchronizedTriggers['Time(s)'].append(time)
                self.synchronizedTriggers['Event'].append(t['Event'])
                self.keepedTriggers['LeftBoundary'].append(left)
                self.keepedTriggers['RightBoundary'].append(right)
                self.keepedTriggers['Trigger'].append(t['Time(s)'])
                self.keepedTriggers['Event'].append(t['Event'])

            elif index == lastIdx:
                time += right - t['Time(s)']
                self.synchronizedTriggers['Time(s)'].append(time)
                self.synchronizedTriggers['Event'].append(t['Event'])
                self.keepedTriggers['LeftBoundary'].append(left)
                self.keepedTriggers['RightBoundary'].append(right)
                self.keepedTriggers['Trigger'].append(t['Time(s)'])
                self.keepedTriggers['Event'].append(t['Event'])

            else:
                time += t['Time(s)'] - prevTrig['Time(s)']
                prevTrig = t
                self.synchronizedTriggers['Time(s)'].append(time)
                self.synchronizedTriggers['Event'].append(t['Event'])
                self.keepedTriggers['LeftBoundary'].append(left)
                self.keepedTriggers['RightBoundary'].append(right)
                self.keepedTriggers['Trigger'].append(t['Time(s)'])
                self.keepedTriggers['Event'].append(t['Event'])

        return time
            
    def __str__(self):
        return pprint.pformat({"Synchronized" : pd.DataFrame(self.synchronizedTriggers).head(n=20), "Keeped" : pd.DataFrame(self.keepedTriggers).head(n=20),"Rejected" : pd.DataFrame(self.rejectedTriggers).head(n=20)})
    
    def triggersCoverage(self):
        return pprint.pformat({"Keeped" : len(self.keepedTriggers['Trigger'])/len(self.triggers.index)*100, "Rejected" : len(self.rejectedTriggers['Event'])/len(self.triggers.index)*100})

if __name__ == "__main__":
    t = ''
    a = ''   
    s = Synchronizer()
    s.importFiles(t,a)
    s.synchronizeTriggersTime()
    o = ''
    s.exportSynchronizedTriggers(o)
    print(s.triggersCoverage())





