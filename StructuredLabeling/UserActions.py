#!/usr/bin/python

import csv
import glob
import xml.etree.ElementTree as ET

def writeCSV(filename, userConditions):
	with open(filename, 'wb') as logfile:
		logwriter = csv.writer(logfile)

		logwriter.writerow(['UserID', 'Condition', 'Order', 'Concept', 
			'createCluster', 'createCluster1st', 'createCluster2nd', 
			'clusterDescriptionChanged', 'clusterDescriptionChanged1st', 'clusterDescriptionChanged2nd',
			'clusterSelected', 'clusterSelected1st', 'clusterSelected2nd', 
			'clusterItemSelected', 'clusterItemSelected1st', 'clusterItemSelected2nd', 
			'movedCluster', 'movedCluster1st', 'movedCluster2nd', 
			'movedClusterToPositive', 'movedClusterToNegative', 'movedClusterToMaybe',
			'movedClusterFromPositive', 'movedClusterFromNegative', 'movedClusterFromMaybe',
			'itemMovedToCluster', 'itemMovedToCluster1st', 'itemMovedToCluster2nd'
			])
		for ucKey in userConditions:
			data = userConditions[ucKey]
			logwriter.writerow([data['userID'], data['condition'], data['order'], data['concept'],
				data['createCluster'], data['createCluster1st'], data['createCluster2nd'], 
				data['clusterDescriptionChanged'], data['clusterDescriptionChanged1st'], data['clusterDescriptionChanged2nd'], 
				data['clusterSelected'], data['clusterSelected1st'], data['clusterSelected2nd'],
				data['clusterItemSelected'], data['clusterItemSelected1st'], data['clusterItemSelected2nd'], 
				data['movedCluster'], data['movedCluster1st'], data['movedCluster2nd'], 
				data['movedClusterToPositive'], data['movedClusterToNegative'], data['movedClusterToMaybe'],
				data['movedClusterFromPositive'], data['movedClusterFromNegative'], data['movedClusterFromMaybe'],
				data['itemMovedToCluster'], data['itemMovedToCluster1st'], data['itemMovedToCluster2nd']
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
		'createCluster':0, 'createCluster1st':0, 'createCluster2nd':0, 
		'clusterDescriptionChanged':0, 'clusterDescriptionChanged1st':0, 'clusterDescriptionChanged2nd':0,
		'clusterSelected':0, 'clusterSelected1st':0, 'clusterSelected2nd':0,
		'clusterItemSelected':0, 'clusterItemSelected1st':0, 'clusterItemSelected2nd':0,
		'movedCluster':0, 'movedCluster1st':0, 'movedCluster2nd':0,
		'movedClusterToPositive':0, 'movedClusterToNegative':0, 'movedClusterToMaybe':0,
		'movedClusterFromPositive':0, 'movedClusterFromNegative':0, 'movedClusterFromMaybe':0,
		'itemMovedToCluster':0, 'itemMovedToCluster1st':0, 'itemMovedToCluster2nd':0
		})

	itemNum = 0
	halfway = 54
	for actions in root.iter('actions'):
		for condition in actions.iter('condition'):
			for action in condition:
				if action.tag == 'createCluster':
					userConditions[ucKey]['createCluster'] += 1
					if itemNum < halfway:
						userConditions[ucKey]['createCluster1st'] += 1
					else:
						userConditions[ucKey]['createCluster2nd'] += 1
				elif action.tag == 'clusterDescriptionChanged':
					userConditions[ucKey]['clusterDescriptionChanged'] += 1
					if itemNum < halfway:
						userConditions[ucKey]['clusterDescriptionChanged1st'] += 1
					else:
						userConditions[ucKey]['clusterDescriptionChanged2nd'] += 1
				elif action.tag == 'clusterSelected':
					userConditions[ucKey]['clusterSelected'] += 1
					if itemNum < halfway:
						userConditions[ucKey]['clusterSelected1st'] += 1
					else:
						userConditions[ucKey]['clusterSelected2nd'] += 1
				elif action.tag == 'clusterItemSelected':
					userConditions[ucKey]['clusterItemSelected'] += 1
					if itemNum < halfway:
						userConditions[ucKey]['clusterItemSelected1st'] += 1
					else:
						userConditions[ucKey]['clusterItemSelected2nd'] += 1
				elif action.tag == 'movedCluster':
					userConditions[ucKey]['movedCluster'] += 1
					if itemNum < halfway:
						userConditions[ucKey]['movedCluster1st'] += 1
					else:
						userConditions[ucKey]['movedCluster2nd'] += 1
					# Figure out how they relabeled the cluster
					if action.attrib['newType'] == 'Positive':
						userConditions[ucKey]['movedClusterToPositive'] += 1
					elif action.attrib['newType'] == 'Negative':
						userConditions[ucKey]['movedClusterToNegative'] += 1
					elif action.attrib['newType'] == 'Maybe':
						userConditions[ucKey]['movedClusterToMaybe'] += 1
					if action.attrib['oldType'] == 'Positive':
						userConditions[ucKey]['movedClusterFromPositive'] += 1
					elif action.attrib['oldType'] == 'Negative':
						userConditions[ucKey]['movedClusterFromNegative'] += 1
					elif action.attrib['oldType'] == 'Maybe':
						userConditions[ucKey]['movedClusterFromMaybe'] += 1
				elif action.tag == 'itemMovedToCluster':
					userConditions[ucKey]['itemMovedToCluster'] += 1
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