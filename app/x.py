def flame():
    return 1

data = {
    flame: []
}

def add_sensor(fn, interval, name):
    sleep(interval)
    data = [name] = fn()

add_sensor(flame, 1/1000, "flame")
