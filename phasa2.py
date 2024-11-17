import halfmarathon


alldist = 60 # недельный обЪем, км
repeats_1_plan = ((200, 200), (200, 400), (400, 200))
repeats_2_plan = ((200, 200),)
threshold_interval = 1.6 # дистанция порогового интервала, км
threshold_pace = "5:45" # пороговый темп


p = halfmarathon.Phase2(alldist)

# Параметры второй тренировки Пв (вместе с П-темпом)
th = p.number_episodes_threshold(threshold_interval, threshold_pace)
print(th[2], th[0], th[1])

rep1 = p.number_episodes_repeats(repeats_1_plan, 1)
rep2 = p.number_episodes_repeats(repeats_2_plan, 2)




    


