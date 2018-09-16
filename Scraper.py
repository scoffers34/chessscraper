# libraries that may need to be required: 
# requests
# beautifulsoup4
#

def RatingGetter(id):
# function that grabs rating of a player with id given in input
	import requests
	id=str(id)

	junk="http://www.uschess.org/msa/MbrDtlMain.php?"
	#uschess player lookup base url, player specifc url is junk+id
	page = requests.get(junk+id)

	from bs4 import BeautifulSoup
	#get BS4 for grabbing webpage
	soup = BeautifulSoup(page.content, 'html.parser')
	#get str version of uschess player page
	l=list(soup.children)
	#grab just text portion
	body=list(soup.children)[7]
	#grab specific partition
	regularrating= body.find("nobr")
	#find player rating, in type nobr on uschess page
	rating = regularrating.contents[0]
	#grab just the rating, regularrating also contains text type info
	rating= str(rating)
	#convert from bs4str to regular str
	return(rating.split()[0])
	
class Tournament(object):
# create tournament object with variables, name, date, player, and player before/after ratings
	def __init__(self,TournName,Date,RegRatingBefore,RegRatingAfter):
		self.Name = TournName
		self.Date = Date
		self.BeforeRating=RegRatingBefore
		self.AfterRating=RegRatingAfter
			
def make_tournament(name, date, oldrating, newrating):
#make a tournament with given variables
	tourni= Tournament(name, date, oldrating, newrating)
	return(tourni)
	
def Tourncleaner(tourns):
#create tournaments list of tournament objects containing name,date,ratings
	#with open("Output.txt","w") as text_file:
	#	text_file.write(tourns)
	tournaments=[]
	t=tourns.splitlines()
	for line in t:
		#print (line)
		#print (type(line))
		#print ("**********")
		#find tournament date, name, rating changes
		d=""
		name=""
		ratingchange=""
		oldrating=""
		newrating=""
		tindex=0
		#print (line[0:2])
		if line[0:2] == "20":
			d = line[0:10]
			tindex=t.index(line)
			#print(tindex)
			#print(d)
			name = t[tindex+1]
			#print(name)
			ratingchange = t[tindex+2]
			oldrating = ratingchange[0:3]
			#print(oldrating)
			newrating = ratingchange[8:]
			#print(newrating)
			
			tournaments.append(make_tournament(name,d,oldrating,newrating))
		# print ("**********")		
		

	
	return(tournaments)	
	
	
def TournHist(id):
#grab tournament history from chess.com for player with id
	import requests
	id=str(id)
	
	tournhist="http://www.uschess.org/msa/MbrDtlTnmtHst.php?"
	page = requests.get(tournhist+id)
	from bs4 import BeautifulSoup
	soup=BeautifulSoup(page.content, 'html.parser')
	
	
	tournaments= soup.get_text()
	tournamentlist=Tourncleaner(tournaments)

	return(tournamentlist)
	
def historywriter(playername, playerHist):
# write output txt file of tournament history
	outputhistoryfile=playername+'.txt'
	f=open(outputhistoryfile, 'w')
	for ts in playerHist:
		f.write (ts.Name+","+ts.Date+","+ts.AfterRating+","+'\n')
	f.close()	

def getplayerlist(playerlist):
# get player and id list from csv file
	players = []
	import csv
	with open(playerlist) as csvfile:
		pl = csv.reader(csvfile, delimiter=',')
		for row in pl:
		#	print (row[0])
			players.append(row)
		#print(players)	
	return (players)
	
# def reportcardprint(players):
	# take txt player tournament histories, and merge into one master list
	# import csv
	# create master tournament list, with dates
	# tournamentlist=[]
	# for player in players:
		# filename=player[0]+'.txt'
		# f=open(filename, 'r')
		# for row in f:
			# if row.split(',')[0] in tournamentlist:
				# print (row.split(',')[0] + ' is already in tournament list')
				# print (row)
			# else:
				# tournamentlist.append(row.split(',')[0]+ ',' + row.split(',')[1])
		# f.close()
	# add player ratings to tournamentlist
	
	for tournament in tournamentlist:
		for player in players:
			f=open(player[0]+'.txt')
			print(type(tournament))
			if (tournament.split(',')[0] in f.split(',')[0]):			
				print('tournament in playerlist')
				for tourn in f:
					if (tournament.split(',')[0] == tourn.split(',')[0]):
						print('adding tournament rating')
						tournament=tournament+','+tourn[2]
			else:
				print('adding blank')
				tournament=tournament+', ,'
			
	t=open('tournamentlist.txt', 'w')
	for ts in tournamentlist:
		t.write (ts + '\n')
	t.close()	
	
	#populate ratings
	return(tournamentlist)
	
def playerratingchart(players):
# write output txt file of tournament history
	ratingchartname=input("What would you like to name the rating chart?")
	outputhistoryfile=ratingchartname+'.txt'
	f=open(outputhistoryfile, 'w')
	for player in players:
		f.write (player[0] + " , " + RatingGetter(player[1])+'\n')
	f.close()	
	
	
	
def main():
	import sys
	#SeansID=12767679
	#playername=input("Player Name, please: ")
	#playerid=input("Player ID, please: ")
	MasterTournHist=[]
	player_list=input("what's the player list file?")
	players = getplayerlist(player_list)
	playerratingchart(players)
	
	for player in players:
		rating=RatingGetter(player[1])
		playerHist=TournHist(player[1])
		MasterTournHist.append(playerHist)
		historywriter(player[0],playerHist)
	

	
	#test = reportcardprint(players)	
	#SeansRating=RatingGetter(SeansID)
	#playerHist=TournHist(playerid)
	#historywriter(playername, playerHist)
	#print (players[0][0])
	#for l in MasterTournHist:
	#	print(l) 
if __name__ == "__main__":
	main()