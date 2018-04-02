import pandas as pd


class Synchronizer:
    def __init__(self):
        self.synchronizedTriggers = {"Time(s)":[],"Event":[]}
        self.triggersTracking = {"LeftBoundary" : [],"RightBoundary":[],"Trigger":[]}
    
    def synchronizeTriggersTime(self):
        deltaStartEnd = 0
        deltaEndStart = 0
        actualTime = 0
        for index,row in artifacts.iterrows():
            
            trig = triggers[(triggers['Time(s)'] >= row['Startkeep(s)']) & (triggers['Time(s)'] <= row['Endkeep(s)'])]
            b = {
                'left' : row['Startkeep(s)'],
                'right' : row['Endkeep(s)']
                }
            if not trig.empty: actualTime += self.testTrigger(actualTime,b, trig)
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

    '''        if not trig.empty:
                #start to trigger then trigger to END
                deltaStartToTrigger = trig['Time(s)'].values[0] - row['Startkeep(s)']
                deltaTriggerToEnd = row['Endkeep(s)'] - trig['Time(s)'].values[0]
                # Computing the new trigger time
                newTrigg = actualTime + deltaStartToTrigger
                
                df['Time(s)'].append(newTrigg)
                df['Event'].append(trig['Event'].values[0])
                
                print("Time is : %s | trigger at : %s | oldStart : %s | oldTrig : %s" % (actualTime,newTrigg,row['Startkeep(s)'],trig['Time(s)'].values[0]))
                if index+1 in artifacts['Startkeep(s)'].index:
                    #if the next row exist, we can obtain the delta between the actual Endkeep and the next start
                    deltaEndToStart = artifacts['Startkeep(s)'][index+1] - row['Endkeep(s)']
                    actualTime+=deltaStartToTrigger + deltaTriggerToEnd + deltaEndToStart
                    
                else:
                    actualTime+=deltaStartToTrigger + deltaTriggerToEnd
                    
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
                    
                print("Time is : %s | trigger at : %s | oldStart : %s | oldTrig : %s" % (actualTime,"No Trigger",row['Startkeep(s)'],"No Trigger"))
    
    def exportSynchronizedTriggers(path,dataframe):
        writer = pd.ExcelWriter(path)
        pd.DataFrame(data=dataframe).to_excel(writer, 'Triggers',index=False)
        writer.save()
    '''
    def testTrigger(self,time,borne,trigs):
        left = borne['left']
        right = borne['right']
        prevTrig = "";
        lastIdx = trigs.index[-1]
        for index,t in triggers.iterrows():
            if index == 0:
                prevTrig = t
                time += t['Time(s)'] - left
                self.synchronizedTriggers['Time(s)'].append(time)
                self.synchronizedTriggers['Event'].append(t['Event'])
                self.triggersTracking['LeftBoundary'].append(left)
                self.triggersTracking['RightBoundary'].append(right)
                self.triggersTracking['Trigger'].append(t['Time(s)'])
            elif index == lastIdx:
                time += right - t['Time(s)']
                self.synchronizedTriggers['Time(s)'].append(time)
                self.synchronizedTriggers['Event'].append(t['Event'])
                self.triggersTracking['RightBoundary'].append(right)
                self.triggersTracking['Trigger'].append(t['Time(s)'])
            else:
                time += t['Time(s)'] - prevTrig['Time(s)']
                prevTrig = t
                self.synchronizedTriggers['Time(s)'].append(time)
                self.synchronizedTriggers['Event'].append(t['Event'])
                self.triggersTracking['RightBoundary'].append(right)
                self.triggersTracking['Trigger'].append(t['Time(s)'])
        return time
            
    def __toString__(self):
        print()        
    
triggers = pd.read_excel('H:/Script_Elo/New_files/triggers_CP15_SAB_6_7_8_Oddball_vis.xlsx')
artifacts = pd.read_excel('H:/Script_Elo/New_files/artefacts_CP15_SAB_6_7_8_Oddball_vis.xlsx')
s = Synchronizer()
s.synchronizeTriggersTime()
#exportSynchronizedTriggers('H:/Script_Elo/triggers_AA20_stim_s2_Synchronized.xlsx', df)




