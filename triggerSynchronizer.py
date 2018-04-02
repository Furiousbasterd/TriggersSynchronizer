import pandas as pd
import pprint


class Synchronizer:
    def __init__(self):
        self.synchronizedTriggers = {"Time(s)":[],"Event":[]}
        self.keepedTriggers = {"LeftBoundary" : [],"RightBoundary":[],"Trigger":[],"Event" : []}
        self.rejectedTriggers = {}
        self.toDrop = []
    
    def synchronizeTriggersTime(self):
        deltaStartEnd = 0
        deltaEndStart = 0
        actualTime = 0
        for index,row in artifacts.iterrows():
            
            trigToKeep = triggers[(triggers['Time(s)'] >= row['Startkeep(s)']) & (triggers['Time(s)'] <= row['Endkeep(s)'])]
            b = {
                'left' : row['Startkeep(s)'],
                'right' : row['Endkeep(s)']
                }

            if not trigToKeep.empty: actualTime = self.testTrigger(actualTime,b, trigToKeep)
            else:
                # Calculating delta between Start and End of the row
                deltaStartEnd = row['Endkeep(s)'] - row['Startkeep(s)']
                # Testing if there is a next row
                if index+1 in artifacts['Startkeep(s)'].index:
                    #if the next row exist, we can obtain the delta between the actual Endkeep and the next start
                    deltaEndStart = artifacts['Startkeep(s)'][index+1] - row['Endkeep(s)']
                    actualTime+=deltaStartEnd + deltaEndStart
                    
                else:
                    # if it does not, only the Start-end delta is added to the actual time
                    actualTime+=deltaStartEnd
        self.rejectedTriggers = triggers.drop(self.toDrop)

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
                #print(str(index)+ " | "+t['Event'])
            elif index == lastIdx:
                time += right - t['Time(s)']
                self.synchronizedTriggers['Time(s)'].append(time)
                self.synchronizedTriggers['Event'].append(t['Event'])
                self.keepedTriggers['LeftBoundary'].append(left)
                self.keepedTriggers['RightBoundary'].append(right)
                self.keepedTriggers['Trigger'].append(t['Time(s)'])
                self.keepedTriggers['Event'].append(t['Event'])
                #print(str(index)+ " | "+t['Event'])
            else:
                time += t['Time(s)'] - prevTrig['Time(s)']
                prevTrig = t
                self.synchronizedTriggers['Time(s)'].append(time)
                self.synchronizedTriggers['Event'].append(t['Event'])
                self.keepedTriggers['LeftBoundary'].append(left)
                self.keepedTriggers['RightBoundary'].append(right)
                self.keepedTriggers['Trigger'].append(t['Time(s)'])
                self.keepedTriggers['Event'].append(t['Event'])
                #print(str(index)+ " | "+t['Event'])
            #print(prevTrig)
        return time
            
    def __str__(self):
        return pprint.pformat({"Synchronized" : pd.DataFrame(self.synchronizedTriggers).head(n=20), "Keeped" : pd.DataFrame(self.keepedTriggers).head(n=20),"Rejected" : pd.DataFrame(self.rejectedTriggers).head(n=20)})
    
    def triggersCoverage(self):
        return {"Keeped" : len(self.keepedTriggers['Trigger'])/len(triggers.index)*100, "Rejected" : len(self.rejectedTriggers['Event'])/len(triggers.index)*100}
    
triggers = pd.read_excel('H:/Script_Elo/New_files/triggers_CP15_SAB_6_7_8_Oddball_vis.xlsx')
artifacts = pd.read_excel('H:/Script_Elo/New_files/artefacts_CP15_SAB_6_7_8_Oddball_vis.xlsx')
s = Synchronizer()
s.synchronizeTriggersTime()
#s.exportSynchronizedTriggers('H:/Script_Elo/New_files/Synchronized_triggers.xlsx')
print(s.triggersCoverage())
#exportSynchronizedTriggers('H:/Script_Elo/triggers_AA20_stim_s2_Synchronized.xlsx', df)




