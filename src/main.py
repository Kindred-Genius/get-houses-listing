import puts3
import insert_dynamodb
#
import agences.arthur_immo
import agences.agence_bizy
import agences.auparkimmo
import agences.century
import agences.demeures_normandes
import agences.desjardins
import agences.ifc_conseil
import agences.joubeaux
import agences.laforet
import agences.laref
import agences.lesage
import agences.orpi
import agences.plaza
import agences.safti
import agences.square_habitat
import agences.vernon_immo

agences.agence_bizy.init()
agences.arthur_immo.init()
agences.auparkimmo.init()
agences.century.init()
agences.demeures_normandes.init()
agences.desjardins.init()
agences.ifc_conseil.init()
agences.joubeaux.init()
agences.laforet.init()
agences.laref.init()
agences.lesage.init()
agences.square_habitat.init()
agences.plaza.init()
agences.vernon_immo.init()

# 
# agences.safti.init()
# agences.orpi.init()
# 

puts3.put_csv_s3()

#
#
insert_dynamodb.analyze_agence()
#
#

