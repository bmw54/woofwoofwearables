
import numpy as np

 
data = {
  "-MyJUUHE8eay7UEi-rdT" : {
    "Time" : 1.6474637566701076E9,
    "Value" : 0.05746083984375
  },
  "-MyJUUpiiXpSoZO-V8ZU" : {
    "Time" : 1.6474637591741593E9,
    "Value" : 0.01915361328125
  },
  "-MyJUVO44lijNEPAIE0Q" : {
    "Time" : 1.647463761435853E9,
    "Value" : 0.00239420166015625
  },
  "-MyJUVwNcXCO46CWxCKm" : {
    "Time" : 1.6474637636954043E9,
    "Value" : 0.047884033203124995
  },
  "-MyJUWUcSM8ToX6NxT3z" : {
    "Time" : 1.6474637659522614E9,
    "Value" : 0.062249243164062495
  },
  "-MyJUX2-Gy9QgLWIP6Il" : {
    "Time" : 1.6474637682150643E9,
    "Value" : 0.016759411621093748
  },
  "-MyJUXaOPLlnXzm4fxi-" : {
    "Time" : 1.6474637704797685E9,
    "Value" : 0.03591302490234375
  },
  "-MyJUY8h_t1cbeb9tmib" : {
    "Time" : 1.6474637727406306E9,
    "Value" : 0.0383072265625
  },
  "-MyJUYgvWIchT2GCncLh" : {
    "Time" : 1.6474637749955509E9,
    "Value" : -0.0047884033203125
  },
  "-MyJUZG5hHd9CNuF4Zb5" : {
    "Time" : 1.6474637773112826E9,
    "Value" : -0.00718260498046875
  },
  "-MyJUZoPAS9sozjeza-I" : {
    "Time" : 1.6474637795704067E9,
    "Value" : -0.02154781494140625
  },
  "-MyJU_MjaDeEP1HV6E9r" : {
    "Time" : 1.6474637818310227E9,
    "Value" : 0.0430956298828125
  },
  "-MyJU_v3zcXqpQjso4-1" : {
    "Time" : 1.6474637840908012E9,
    "Value" : -0.0143652099609375
  },
  "-MyJUaTM0Jb2dL31wqHe" : {
    "Time" : 1.6474637863504553E9,
    "Value" : 0.023942016601562498
  },
  "-MyJUb0aUcjBtXcwauRq" : {
    "Time" : 1.647463788607067E9,
    "Value" : 0.05746083984375
  },
  "-MyJUbZwzKatDzUDg9KQ" : {
    "Time" : 1.6474637908679276E9,
    "Value" : 0.055066638183593745
  },
  "-MyJUc7BWxZscbn3yLDX" : {
    "Time" : 1.6474637931271183E9,
    "Value" : 0.05027823486328125
  },
  "-MyJUcfS_E-8g1d8mKPX" : {
    "Time" : 1.6474637953819742E9,
    "Value" : 0.02154781494140625
  },
  "-MyJUdDrcgXl4nvtZKCP" : {
    "Time" : 1.6474637976410294E9,
    "Value" : 0.0430956298828125
  },
  "-MyJUdm9FxQM9sXBMlm-" : {
    "Time" : 1.6474637999071376E9,
    "Value" : 0.0430956298828125
  },
  "-MyJUeKP4HdQ3PrCTKeV" : {
    "Time" : 1.647463802162398E9,
    "Value" : 0.009576806640625
  },
  "-MyJUescERDbBdXTdolW" : {
    "Time" : 1.647463804417978E9,
    "Value" : -0.03591302490234375
  },
  "-MyJUfQxJ3Je_b46M8B5" : {
    "Time" : 1.6474638066769753E9,
    "Value" : 0.06464344482421874
  },
  "-MyJUfzALjC92Nw38Mjc" : {
    "Time" : 1.6474638089317489E9,
    "Value" : 0.047884033203124995
  },
  "-MyJUgXPFls7yETcVWvV" : {
    "Time" : 1.6474638111879709E9,
    "Value" : 0.03591302490234375
  },
  "-MyJUh917uqWDhORHK7a" : {
    "Time" : 1.6474638134525542E9,
    "Value" : 0.03591302490234375
  },
  "-MyJUhh4PWt-JU1cN4F2" : {
    "Time" : 1.647463815963694E9,
    "Value" : 0.00718260498046875
  },
  "-MyJUiFSP6WP11ZtmrMu" : {
    "Time" : 1.647463818230806E9,
    "Value" : 0.0047884033203125
  },
  "-MyJUinnYViOacxSsqMH" : {
    "Time" : 1.6474638204905741E9,
    "Value" : 0.055066638183593745
  },
  "-MyJUjM4SKcbLzNMqvJl" : {
    "Time" : 1.647463822747912E9,
    "Value" : 0.00239420166015625
  },
  "-MyJUjuL7AN7OnI_5moI" : {
    "Time" : 1.647463825007194E9,
    "Value" : 3.902548706054687
  },
  "-MyJUkSbRFxYE6s8LWHE" : {
    "Time" : 1.647463827263318E9,
    "Value" : 3.948038537597656
  },
  "-MyJUl-qA1PUeFihlNNs" : {
    "Time" : 1.6474638295200937E9,
    "Value" : 3.4165257690429685
  },
  "-MyJUlZ3msX7OTjY-5FO" : {
    "Time" : 1.6474638317741106E9,
    "Value" : 3.385401147460937
  },
  "-MyJUm6J_AbxjL8jsoPa" : {
    "Time" : 1.6474638340305583E9,
    "Value" : 3.3327287109375
  },
  "-MyJUme__Bfb-wmZIILx" : {
    "Time" : 1.6474638362867985E9,
    "Value" : 3.3638533325195312
  },
  "-MyJUnCpNi0uox7JSnIC" : {
    "Time" : 1.647463838541833E9,
    "Value" : 3.3638533325195312
  },
  "-MyJUnl5XdhCDA2cjrmc" : {
    "Time" : 1.6474638407991564E9,
    "Value" : 3.3255461059570313
  },
  "-MyJUoJJoiOEIga2Mh7-" : {
    "Time" : 1.6474638430523152E9,
    "Value" : 3.394977954101562
  },
  "-MyJUoriBvUDH2vjTgiV" : {
    "Time" : 1.647463845318742E9,
    "Value" : 3.3399113159179685
  },
  "-MyJUpQytBBgieM8ad-G" : {
    "Time" : 1.6474638476382904E9,
    "Value" : 3.337517114257812
  },
  "-MyJUpzHx3PHC1mt9u3D" : {
    "Time" : 1.647463849894717E9,
    "Value" : 3.337517114257812
  },
  "-MyJUqYeX7KAeM4vYyCo" : {
    "Time" : 1.6474638522267258E9,
    "Value" : 3.375824340820312
  },
  "-MyJUr628yDNM6glkfNX" : {
    "Time" : 1.6474638544913425E9,
    "Value" : 3.31357509765625
  },
  "-MyJUreKUWfC9PNbUq7Q" : {
    "Time" : 1.6474638567494738E9,
    "Value" : 3.277662072753906
  }
}

data = list(data.values())
timestamps = [d['Time'] for d in data]
ang_velo = [d['Value'] for d in data]

ang_position = np.trapz(ang_velo, x =timestamps )
print(ang_position)


        