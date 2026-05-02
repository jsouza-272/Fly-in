# Parser #
    ver se o parser ta certo
    mudar o check dos metadatas
    mudar colors para a constante do pygame


# Drones #
    fazer o drone se mover
    atualizar a coordenada do drone se ele estiver em uma connection por causa de uma zona restricted
    adicionar uma funcao de recalcular a rota do drone (provavelmente em DroneManeger)
    fazer algo com o setter do node para quando o drone estiver no link
    mudar a funcao walk para ser de um node para outro (def walk(self, to_node: Hub, link_to_use: Link) )
 

# Hub #
    fazer uma flag que diz que esta esperando um drone


# Links #
    fazer algo para resetar so os links que nao estiverem sendo usados
    mudar como funciona quais drones estao nos links


# Emulation #
    fazer a funcao que percorre todos os drones e fala para eles andarem
    fazer uma lista de drones que chegaram no fim


# Simulacao de turnos #
    fazer drone ir para connection se for restricted
    se for restricted o drone demora 2 turnos para chegar ao destino
    nao preciso esperar na um turno na zona o drone demora 2 turnos para passar pelo connection


# GUI #
    usar circulos/quadrados (ver oque fica melhor) para os hub
    usar linhas para as connections
    pensar em como fazer os drones se moverem (talves somar 0.2 se nao for restricted e 0.1 se for)
