import halfmarathon


alldist = 60 # недельный обЪем, км
repeats_1_plan = ((200, 200), (200, 400), (400, 200))
repeats_2_plan = ((200, 200),)


p = halfmarathon.Phase2(alldist)

ner1 = p.number_episodes_repeats(repeats_1_plan, 1)
ner2 = p.number_episodes_repeats(repeats_2_plan, 2)

th = p.number_episodes__threshold(1.6)
print(th)

##for i in ner2:
##    print(i)

    


