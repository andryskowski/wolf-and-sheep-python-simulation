from configparser import ConfigParser

file = 'config.ini'
config = ConfigParser()
config.read(file)

print(config['Terrain']['InitPosLimit'])
print(config['Movement']['SheepMoveDist'])
print(config['Movement']['WolfMoveDist'])