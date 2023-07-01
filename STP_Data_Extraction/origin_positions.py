from OCC.Core.TopLoc import TopLoc_Location
import pandas as pd

class Origin:

    def location(location_references, name):

        loc = TopLoc_Location() #Constructs an empty local coordinate system object
        for l in location_references:
            print("    take loc       :", l)
            loc = loc.Multiplied(l) #essential to get correct x, y, z relative values


        trans = loc.Transformation()
        print("    FINAL loc    :")
        print("    tran form    :", trans.Form())


        # rot = trans.GetRotation()
        # print("    rotation     :", rot)
        # print("    X            :", rot.X())
        # print("    Y            :", rot.Y())
        # print("    Z            :", rot.Z())
        # print("    W            :", rot.W())
        tran = trans.TranslationPart()
        # print("    translation  :", tran)
        # print("    X            :", tran.X())
        # print("    Y            :", tran.Y())
        # print("    Z            :", tran.Z())


        df_row = pd.DataFrame({"Shape Name": [name], "Translation": [tran], "X": [tran.X()], "Y": [tran.Y()], "Z": [tran.Z()]})

        # print(df_row)
        return df_row