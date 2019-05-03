from pygame.mixer import Sound

print("Загрузка звуковых файлов...")

enemy_shoot_sound = Sound('resources/gshoot.wav')
enemy_auch_sound = Sound('resources/gauch.wav')
player_auch_sound = Sound('resources/auch.wav')
player_shoot_sound = Sound('resources/pshoot.wav')
player_walk_sound = Sound('resources/walk.wav')
trap_down_sound = Sound('resources/trapdown.wav')
trap_up_sound = Sound('resources/trapup.wav')
furniture_breaking_sound = Sound('resources/break.wav')
teleport_sound = Sound('resources/teleport.wav')
heal_sound = Sound('resources/heal.wav')

print("Звуковые файлы загружены")
