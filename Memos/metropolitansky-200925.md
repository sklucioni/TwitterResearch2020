**Memo metropolitansky-200925.md**

# Updating Scraper Filters

This memo is about updating our list of filters for the scraper. 

1. I took the Twitter lists Andrew used in his thesis and used the Twitter API to scrape the account names in these lists.
2. I identified several lists that seemed to have a large proportion of redundant accounts. I manually went through those lists and removed accounts who (a) had less than 10K followers, (b) were not tweeting actively, (c) tweeted about things not relevant to politics, and/or (d) received very little response to their tweets. 
3. I manually added accounts that were missing from the previous two steps but which our team deemed important to track. 

See Appendix for more details about the above steps.

The final list contained 2,684 accounts, which is 109 more than the previous version (which had 2,575 accounts). The two lists have 2,192 accounts in common (which is 81.67% of the new list and 85.13% of the old list). 

The updated list went into effect on September 19. 

# Appendix

### List-by-list breakdown

**TwitterGov**
- us-house - updated
- us-senate - updated
- us-cabinet - updated
- us-cities - updated
- us-election-officials - replaced ‘us-secretaries-of-state’
- us-presidential-candidates - updated
- us-governors - updated

**C-Span**
- political-reporters - updated

**Fox News**
- fox-accounts - updated
- shows-hosts - new
- all-fox-news - reduced

**CNN**
- bestpoliticalteam - replaced ‘cnn-political-team’
- cnn-news - reduced

**MSNBC**
- correspondent-list - updated
- msnbc-shows-and-hosts1 - updated 

**New York Times**
- new-york-times-politics - updated
- elections-2020 - new

**Wall Street Journal** 
- wsj-politics - updated 

**The Washington Post** 
- post-politics - updated

**Slate** 
- right-leaning-tweets - updated
- left-leaning-tweets - updated

**ABC** 
- abc-news-staff - reduced
- politics - updated
- mediaorgs - updated

**NBC News** 
- politics-reporter-embed - replaced ‘politics-reporters-embeds1’
- archive-election-embeds - replaced ‘election-day-embeds’
- nbc-news-msnbc-brands - updated

**CBS News** 
- cbs-news-2020-politics - new
- cbs-news-politics-team - new
- cbs-news-team - reduced

**PunditFact** 
- political-pundits - updated

**Max Temkin** 
- u-s-politics-2020 - replaced ‘u-s-politics-2019’ 

**Matt Lewis** 
- conservatives - new
- liberals - new
- media - new
- political-journalists - updated

**Ari Herzog**
- alt-and-rogue1 - new
- white-house-reporters1 - updated

### Manually added accounts

The main categories of accounts that the team chose to manually add were:
1. Family members of the candidates
2. Prominent political and media figures
3. Candidates in contentious house/senate races
4. Prominent activist/interest groups
5. Media organizations to ensure representation of the entire political spectrum.

Here are the specific accounts:
MichelleObama, DrBiden, HillaryClinton, AndrewYang, TheDemocrats, HouseDemocrats, JohnKasich, SenateGOP, GOP, charliekirk11, shannonrwatts, IvankaTrump, TiffanyATrump, EricTrump, LaraLeaTrump, POTUS, StephGrisham45, KellyannePolls, FLOTUS, PressSec, SecondLady, QAnon_Report, laurenboebert, DeAnna4Congress, theangiestanton, montaga, mtgreenee, PeteHegseth, Blklivesmatter, PPFA, AMarch4OurLives, Heritage, NRA, theMRC, BillClinton,SarahPalinUSA, StephenBannon, GenFlynn, MichaelCohen212, redsteeze, Scaramucci, Reince, gtconway3d, TTuberville, CaptMarkKelly, Hickenlooper, ossoff, RepDougCollins, ReverendWarnock, GreenfieldIowa, SaraGideon, JohnJamesMI, CalforNC, mjhegar, GinaOrtizJones, TonyGonzales4TX, Carolyn4GA7, RichforGA, RepTorresSmall, Yvette4congress,RepKendraHorn, stephaniebice, BenMcAdams, BurgessOwens, candacefor24, Bethvanduyne, NancyMace, marwilliamson, millermeeks,
RitaHartIA, VoteJackie4NY, GarbarinoforNY, SriPKulkarni, SheriffTNehls, iamjohnoliver, TheDailyShow, Trevornoah, StephenAtHome, hasanminhaj, TuckerCarlson, marklevinshow, dbongino, jonlovett, danpfeiffer, crookedmedia, realBobWoodward, Comey, davidaxelrod, HuffPost, MotherJones, NewYorker, USATODAY, TheEconomist, tweetdrudge, BreitbartNews, theblaze, RealCandaceO, realDailyWire, Alyssa_Milano, jonathanvswan, coldxman, piersmorgan, ezraklein, Mike_Pence, WestWingReport, TeamTrump, MrsVanessaTrump,
DiamondandSilk, GOPChairwoman, TheOnion, ProjectLincoln, RepsForBiden, OANN, WomenforTrump
