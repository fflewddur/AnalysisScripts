#!/usr/bin/python

import csv
import glob
import xml.etree.ElementTree as ET

def writeCSV(filename, userConditions):
	with open(filename, 'wb') as logfile:
		logwriter = csv.writer(logfile)

		logwriter.writerow(['UserID', 'Condition', 'Order', 'Concept', 
			'createCluster1st', 'createCluster2nd', 
			'clusterDescriptionChanged1st', 'clusterDescriptionChanged2nd',
			'clusterSelected1st', 'clusterSelected2nd', 
			'clusterItemSelected1st', 'clusterItemSelected2nd', 
			'movedCluster1st', 'movedCluster2nd', 
			'itemMovedToCluster1st', 'itemMovedToCluster2nd'
			])
		for ucKey in userConditions:
			data = userConditions[ucKey]
			logwriter.writerow([data['userID'], data['condition'], data['order'], data['concept'],
				data['createCluster1st'], data['createCluster2nd'], 
				data['clusterDescriptionChanged1st'], data['clusterDescriptionChanged2nd'], 
				data['clusterSelected1st'], data['clusterSelected2nd'],
				data['clusterItemSelected1st'], data['clusterItemSelected2nd'], 
				data['movedCluster1st'], data['movedCluster2nd'], 
				data['itemMovedToCluster1st'], data['itemMovedToCluster2nd']
				])

def parseLog(filename, userConditions):
	tree = ET.parse(filename)
	root = tree.getroot()
	
	# Root attributes
	user = root.attrib['participantId']
	concept = root.attrib['concept']
	order = root.attrib['order']
	condition = root.attrib['condition']

	ucKey = user + '-' + condition
	if ucKey in userConditions:
		print("Error: " + ucKey + " already exists in dictionary.")
		return

	userConditions[ucKey] = ({'userID':user, 'concept':concept, 'order':order, 'condition':condition,
		'createCluster1st':0, 'createCluster2nd':0, 
		'clusterDescriptionChanged1st':0, 'clusterDescriptionChanged2nd':0,
		'clusterSelected1st':0, 'clusterSelected2nd':0,
		'clusterItemSelected1st':0, 'clusterItemSelected2nd':0,
		'movedCluster1st':0, 'movedCluster2nd':0,
		'itemMovedToCluster1st':0, 'itemMovedToCluster2nd':0
		})

	itemNum = 0
	halfway = 54
	for actions in root.iter('actions'):
		for condition in actions.iter('condition'):
			for action in condition:
				if action.tag == 'createCluster':
					if itemNum < halfway:
						userConditions[ucKey]['createCluster1st'] += 1
					else:
						userConditions[ucKey]['createCluster2nd'] += 1
				elif action.tag == 'clusterDescriptionChanged':
					if itemNum < halfway:
						userConditions[ucKey]['clusterDescriptionChanged1st'] += 1
					else:
						userConditions[ucKey]['clusterDescriptionChanged2nd'] += 1
				elif action.tag == 'clusterSelected':
					if itemNum < halfway:
						userConditions[ucKey]['clusterSelected1st'] += 1
					else:
						userConditions[ucKey]['clusterSelected2nd'] += 1
				elif action.tag == 'clusterItemSelected':
					if itemNum < halfway:
						userConditions[ucKey]['clusterItemSelected1st'] += 1
					else:
						userConditions[ucKey]['clusterItemSelected2nd'] += 1
				elif action.tag == 'movedCluster':
					if itemNum < halfway:
						userConditions[ucKey]['movedCluster1st'] += 1
					else:
						userConditions[ucKey]['movedCluster2nd'] += 1
				elif action.tag == 'itemMovedToCluster':
					if itemNum < halfway:
						userConditions[ucKey]['itemMovedToCluster1st'] += 1
					else:
						userConditions[ucKey]['itemMovedToCluster2nd'] += 1
				elif action.tag == 'itemAddedToCluster':
					itemNum += 1
				elif action.tag == 'unlabeledItemShown':
					pass
				elif action.tag == 'similarItemSelected':
					pass
				else:
					print("Unhandled action: " + action.tag)


def main():
	userConditions = {} # dictionary of each user-condition tuple
	files = glob.glob("/Users/todd/Desktop/ClusterLogs/*.xml")
	print("Reading files...")
	for file in files:
		parseLog(file, userConditions)

	print("Writing CSV file...")
	writeCSV("/Users/todd/Desktop/ClusterLogActions.csv", userConditions)

if __name__ == '__main__':
	main()