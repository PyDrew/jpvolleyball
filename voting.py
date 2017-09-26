import os
import sys
import json

try:
    data_dir = os.environ['OPENSHIFT_DATA_DIR']
except KeyError:
    data_dir = 'static'

def LogVoteAttempt(route):
    fn = os.path.join(data_dir,'attempts.txt')
    if os.path.exists(fn):
        fp = open(os.path.join(data_dir,'attempts.txt'), 'a')
    else:
        fp = open(os.path.join(data_dir,'attempts.txt'), 'w')
    fp.write("%s\n" % str(route))
    fp.close()
    
def AddVote(player, comment, ip):
    vote_file = (os.path.join(data_dir,'votes.json'))
    response = "Thank you for voting!"
    if not os.path.exists(vote_file):
        vote_data = {'votes': {}, 'ip_addresses': []}
        json.dump(vote_data, open(vote_file, 'w'), indent=3)

    vote_data = json.load(open(vote_file))
    
    vote_data["ip_addresses"].append(ip)
    try:
        vote_data['votes'][player]['num_votes'] += 1
    except KeyError:
        vote_data['votes'][player] = {'num_votes': 1}
    
    if comment:
        try:
            vote_data['votes'][player]['comments'].append(comment)
        except:
            vote_data['votes'][player]['comments'] = [comment,]
    json.dump(vote_data, open(vote_file, 'w'), indent=3)

    return response

def ClearVotingIPAddresses():
    vote_file = os.path.join(data_dir, 'votes.json')
    
    if os.path.exists(vote_file):
        vote_data = json.load(open(vote_file))
        vote_data['ip_addresses'] = []
        json.dump(vote_data, open(vote_file, 'w'), indent=3)

def ClearVotingData():
    vote_file = os.path.join(data_dir, 'votes.json')
    
    if os.path.exists(vote_file):
        vote_data = json.load(open(vote_file))
        vote_data['votes'] = {}
        vote_data['ip_addresses'] = []
        json.dump(vote_data, open(vote_file, 'w'), indent=3)

if __name__ == '__main__':
    #AddVote('Drew Marchand', 'Wicked good!', '207.15.202.4')
    if len(sys.argv) > 1:
        if sys.argv[1] == '--clear_ips':
            ClearVotingIPAddresses()
        elif sys.argv[1] == '--clear_data':
            ClearVotingData()
        else:
            print "\nERROR: Did not understand option: %s" % sys.argv[1]
    #ClearVotingData()