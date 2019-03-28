# Love-Nikki-Dress-Up-Queen
Recommendations for outfits used in Love Nikki Stylist Association and Stylist Arena

This script runs using Python 3.

## Usage

Run the script:

```bash
python3 ./nikki.py
```

You will then be asked:
```bash
Stylist arena mode? (Y/N)
```

For `Stylist arena mode`:

```bash
Which theme? (e.g., The Queen, Cloud Lady, etc.)
```

Type in the theme, for example, for `Cloud Lady`:
```
For theme Cloud lady the target stats and weights are:
Gorgeous 1.33
Elegance 1.33
Mature 1.0
Pure 1.33
Warm 0.66
5 stats:  ['Gorgeous', 'Elegance', 'Mature', 'Pure', 'Warm']
```

Then you will be asked if you are looking for a specific item (e.g., shoes), or an outfit:
```
What are you looking for?  Name an item type or "Outfit"
```

You can chose to display or not display items with some wrong stats.
```
Display items with some wrong stats? (Y/N)
```

You can also look for items with specific list of stats by choose No for the `Stylist arena mode` prompt. For example, you are searching for outfits with the 5 stats `Simple, Elegance, Mature, Pure, Warm`:

```
Stylist arena mode? (Y/N) N
Stats you are looking for (e.g., Simple, Lively, Cute): Simple, Elegance, Mature, Pure, Warm  
```

Next you will be asked if you are looking for a specific `Tags`, let's say, for example, `Fairy`.
```
Tags you are looking for (e.g., Rock, Fairy, Kimono): Rock
```

Again, you may be looking for a specific item or an outfit, for example, a dress.
```
What are you looking for?  Name an item type or "Outfit":  Dress
```

You will be asked if you want to assign different weights for each stat, and if you want to display items with some wrong stats. The default is No.
```
Scoring with different weights? (Y/N)
Display items with some wrong stats? (Y/N) 
```



