"""
For unmatched WhoScored players, finds closest name match within same squad - candidates for the nickname dictionary

Usage:
python3 suggest_name_matches.py
"""
import difflib
import pandas as pd

players = pd.read_csv("data/all_players.csv")

# paste the unmatched list here (Player, Squad pairs)
unmatched = [
    ("Abdul Fatawu", "Leicester City"),
    ("Benjamin Whiteman", "Preston"),
    ("Jaden Philogene", "Ipswich Town"),
    ("Mattie Pollock", "Watford"),
    ("Mohamed Belloumi", "Hull City"),
    ("Ben Chrisene", "Norwich City"),
    ("Kayne Ramsay", "Charlton Athletic"),
    ("Andri Gudjohnsen", "Blackburn"),
    ("Emil Riis", "Bristol City"),
    ("Joshua Key", "Swansea City"),
    ("Nathan Wood", "Southampton"),
    ("Eric-Junior Bocat", "Stoke City"),
    ("Bailey Cadamarteri", "Sheffield Weds"),
    ("David Akintola", "Hull City"),
    ("Kaly Sène", "Middlesbrough"),
    ("Mohamed Alì Zoma", "Nürnberg"),
    ("Baris Atik", "Magdeburg"),
    ("Berkay Yilmaz", "Nürnberg"),
    ("Michaël Cuisance", "Hertha BSC"),
    ("Mika Haas", "Kaiserslautern"),
    ("Laurin Ulrich", "Magdeburg"),
    ("Noël Aséko", "Hannover 96"),
    ("Oliver Batista Meier", "Preußen Münster"),
    ("Stefán Thórdarson", "Hannover 96"),
    ("Finn Becker", "Nürnberg"),
    ("Luca Schuler", "Hertha BSC"),
    ("Pape Diop", "Nürnberg"),
    ("Kim Ji-Soo", "Kaiserslautern"),
    ("Jonas Kersken", "Arminia"),
    ("Luca Itter", "Greuther Fürth"),
    ("Sima Suso", "Düsseldorf"),
    ("Rafael Pedrosa", "Karlsruher"),
    ("Charalambos Makridis", "Preußen Münster"),
    ("Marvin Marcel Schulz", "Preußen Münster"),
    ("Jón Dagur Thorsteinsson", "Hertha BSC"),
    ("William Kokolo", "Hannover 96"),
    ("Kjell Wätjen", "Bochum"),
    ("Zaid Tchibara", "Schalke 04"),
    ("Owono-Darnell Keumo", "Bochum"),
    ("Kenny Prince Redondo", "Kaiserslautern"),
    ("Boris Mamuzah Lum", "Hertha BSC"),
    ("Afeez Aremu", "Kaiserslautern"),
    ("Noah Maboulou", "Nürnberg"),
    ("Juan Cabrera", "Greuther Fürth"),
    ("Ali Eren Ersungur", "Karlsruher"),
    ("Kwon Hyeok-Kyu", "Karlsruher"),
    ("Marvin Rittmüller", "BTSV"),
    ("Justin Heekeren", "Schalke 04"),
    ("Niclas Thiede", "Bochum"),
    ("Tim Boss", "Elversberg"),
    ("Grant-Leon Ranos", "BTSV"),
    ("Serhat-Semih Güler", "Darmstadt 98"),
    ("John Anthony Brooks", "Hertha BSC"),
]

for name, squad in unmatched:
    squad_players = players[players["Squad"] == squad]["Player"].tolist()
    if not squad_players:
        print(f"{name} ({squad}): no players found for this squad at all - check squad name")
        continue
    close = difflib.get_close_matches(name, squad_players, n=1, cutoff=0.5)
    if close:
        print(f"{name} ({squad}) -> possible match: {close[0]}")
    else:
        print(f"{name} ({squad}) -> no close match found (may be a genuinely missing/fringe player)")