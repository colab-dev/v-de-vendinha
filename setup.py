import cx_Freeze

executables = [cx_Freeze.Executable("app.py")]

cx_Freeze.setup(
  name = "V de Vendinha",
  options = {"build_exe":{
    "packages":["pygame"],
    "include_files":[
      "./resources/images/GroceryShelf.png",
      "./resources/images/brocolis.png",
      "./resources/images/eggplant.png",
      "./resources/images/onion.png",
      "./resources/images/bell-pepper.png",
      "./resources/images/beef.png",
      "./resources/images/cheese.png",
      "./resources/images/chicken.png",
      "./resources/audio/background.wav",
      "./resources/audio/fail.wav",
      "./resources/audio/gameover.wav"]}
  },
  description = "Jogo V de Vendinha",
  executables = executables
)
