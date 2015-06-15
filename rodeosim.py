#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:peckj.20150615142156.1: * @file rodeosim.py
#@@first
#@@language python

''' rodeosim.py - simulates a rodeo for a solo game of 8 Seconds From Glory. '''

#@+<< imports >>
#@+node:peckj.20150615142304.1: ** << imports >>
import random
#@-<< imports >>
#@+<< declarations >>
#@+node:peckj.20150615142308.1: ** << declarations >>
#@+others
#@+node:peckj.20150615150154.1: *3* NPR tables
# NPR - A table
NPR_A = {3:[False, 0, 0], 4:[False, 0, 0], 
         5: [False, 0, 0], 6: [False, 0, 0],
         7: [False, 0, 0], 8: [True, 1, 0],
         9: [True, 1, 0], 10: [True, 2, 1],
         11: [True, 2, 1], 12: [True, 2, 1]}

# NPR - B table
NPR_B = {3:[False, 0, 0], 4:[False, 0, 0], 
         5: [False, 0, 0], 6: [False, 0, 0],
         7: [False, 0, 0], 8: [False, 0, 0],
         9: [True, 1, 0], 10: [True, 1, 0],
         11: [True, 2, 1], 12: [True, 2, 1]}

# NPR - Lean table
NPR_LEAN = {1: 'F', 2: 'R', 3: 'B', 4: 'L', 5: 'Bull', 6:'Bull'}
#@+node:peckj.20150615150138.1: *3* Bull tables
# Bull Maneuver table
BULL_MANEUVER = {6: ('B',3), 7: ('F',4),
                 8: ('B',3), 9: ('F',4),
                 10: ('B',4), 11: ('B',4),
                 12: ('F',5), 13: ('S',7),
                 14: ('S',7), 15: ('S',8),
                 16: ('SF',8),17: ('SF',9),
                 18: ('SF',10)}

def BULL_SPIN(value, spin):
  if value <= 5:
    if spin == 'L': 
      return 'R'
    else:
      return 'L'
  else:
    return spin
#@-others

#@-<< declarations >>

#@+others
#@+node:peckj.20150615142417.1: ** class Bull
class Bull:
  def __init__(self, ID, rep, spin, power, agility, speed):
    self.ID = ID
    self.rep = rep
    self.spin = spin
    self.power = power
    self.agility = agility
    self.speed = speed
    self.points = 0
    self.prev_spin = None
#@+node:peckj.20150615142426.1: ** class Rider
class Rider:
  def __init__(self, ID, rep, guts, skill, strength):
    self.ID = ID
    self.rep = rep
    self.guts = guts
    self.skill = skill
    self.strength = strength
    self.ride_dice = self.rep * 2
    self.score = 0
    
    # temp stuff
    self.points = 0
    self.guts_loss = False
    self.str_loss = False
  
  def __str__(self):
    return "%s: (%s,%s,%s,%s,%s)" % (self.ID, self.rep, self.guts, self.skill, self.strength, self.ride_dice)
    
#@+node:peckj.20150615143836.1: ** roll
def roll(n=1):
  return sorted([random.randint(1,6) for _ in range(n)])
#@+node:peckj.20150615150924.1: ** count_successes
def count_successes(dice):
  return dice.count(1) + dice.count(2) + dice.count(3)
#@+node:peckj.20150615142729.1: ** main
def main():
  bulls = {2: Bull(401,4,'L',4,3,1),
           3: Bull(420,4,'R',5,2,1),
           4: Bull(439,4,'L',4,1,3),
           5: Bull(445,4,'R',2,3,3),
           6: Bull(476,4,'L',5,1,2),
           7: Bull(485,4,'R',2,3,3),
           8: Bull(509,5,'L',4,3,3),
           9: Bull(542,5,'R',5,3,2),
           10: Bull(554,5,'L',5,1,4),
           11: Bull(652,6,'R',6,2,4),
           12: Bull(666,6,'L',6,3,3)}
  
  riders = {2: Rider('Abe',3,3,2,1),
            3: Rider('Billy',3,2,2,2),
            4: Rider('Charlie',3,2,3,1),
            5: Rider('Doug',4,2,3,3),
            6: Rider('Ed',4,2,4,2),
            7: Rider('Frank',4,3,3,2),
            8: Rider('George',4,3,2,3),
            9: Rider('Henry',5,4,2,4),
            10: Rider('Indigo',5,5,3,2),
            11: Rider('Jones',5,2,4,4),
            12: Rider('Kelly',5,3,2,5)}
  
  # generate riders for this game
  rodeo_riders = []
  while len(rodeo_riders) < 9:
    r = riders[sum(roll(2))]
    if r not in rodeo_riders:
      rodeo_riders.append(r)
  
  # run two rides with each rider
  for ride in range(2):
    for rider in rodeo_riders:
      run_ride(rider, bulls[sum(roll(2))])
      rider.score += rider.points
      rider.points = 0
      rider.ride_dice = rider.rep * 2
      
  
  # tally scores, sort, and print results
  print '===== Results, after 2 rides ====='
  rodeo_riders = sorted(rodeo_riders, key=lambda r: r.score, reverse=True)
  for rider in rodeo_riders:
    print '%s\t\t%s' % (rider.ID, rider.score)
  
  # prompt for riders in round 2 (third ride)
  choice = raw_input("Run another ride for the top four? ")
  if 'y' in choice.lower():
    # run third ride with each of the round 2 riders
    for rider in rodeo_riders[:4]:
      run_ride(rider, bulls[sum(roll(2))])
      rider.score += rider.points
      rider.points = 0
      rider.ride_dice = rider.rep * 2
    # tally scores, sort, and print results
    print '===== Results, after 3 rides ====='
    rodeo_riders = sorted(rodeo_riders, key=lambda r: r.score, reverse=True)
    for rider in rodeo_riders:
      print '%s\t\t%s' % (rider.ID, rider.score)
  
#@+node:peckj.20150615144408.1: *3* run_ride
def run_ride(rider, bull):
  # break out of the chute
  thrown = False
  rider_dice = count_successes(roll(rider.rep))
  bull_dice = count_successes(roll(bull.rep))
  if bull_dice - rider_dice >= 2:
    thrown = True
  
  # run the ride
  if not thrown:
    for second in range(8,0,-1):
      thrown = run_turn(second, rider,bull)
      if thrown:
        break
  
  # score + thrown results
  if rider.str_loss:
    rider.strength += 1
    rider.str_loss = False
  if thrown:
    rider.points = 0
    
    r_tossed_results = count_successes(roll(rider.rep))
    b_tossed_results = count_successes(roll(bull.rep))
    delta = b_tossed_results - r_tossed_results
    if delta >= 2:
      rider.rep -= 1
      rider.guts -= 1
      rider.guts_loss = True
    elif delta == 1:
      rider.strength -= 1
      rider.str_loss = True
    elif delta == 0:
      # nothing happens, safe landing
      pass
    elif delta == -1:
      rider.strength -= 1
      rider.str_loss = True
    elif delta <= -2:
      # nothing happens, safe landing
      pass
  else:
    if rider.points > 50:
      rider.points = 50
    if bull.points >= 40:
      rider.points += 3 # hard ride bonus
    rider.points += bull.points
    if rider.guts_loss:
      rider.guts += 1
      rider.guts_loss = False
  bull.points = 0
  bull.prev_spin = None
  
  
#@+node:peckj.20150615144713.1: *4* run_turn
def run_turn(second,rider, bull):
  # important variables:
  # lean - rider's lean
  # ride_dice - ride dice expended by rider
  # style_points - points given to the bull
  # bull_spin - current spin direction
  # bull_maneuver - current bull maneuver
  # bull_points - points awarded to the bull
  
  # rider actions
  table = NPR_B
  if rider.ride_dice > second:
    table = NPR_A
  d6 = sum(roll(1)) + rider.rep
  lean = table[d6][0]
  if lean:
    lean = NPR_LEAN[sum(roll(1))]
  
  if second == 1: # ALL IN
    rolled_dice = roll(rider.ride_dice)
    style_points = rolled_dice.count(6)
    ride_dice = rider.ride_dice - style_points
  else:
    d6 = sum(roll(1)) + rider.rep
    ride_dice = table[d6][1]
    if ride_dice > rider.ride_dice:
      ride_dice = 0
    d6 = sum(roll(1)) + rider.rep
    style_points = table[d6][2]
    if style_points > rider.ride_dice:
      style_points = 0
  rider.ride_dice -= (style_points + ride_dice)

  # bull maneuver
  bull_spin = None
  d6 = sum(roll(2)) + bull.rep
  bull_maneuver, bull_points = BULL_MANEUVER[d6]
  bull.points += bull_points
  if bull.points > 50: bull.points = 50
  if bull_maneuver in ['S','SF']:
    mod = 0
    if bull.prev_spin is not None and bull.prev_spin != bull.spin:
      mod = -1
    elif bull.prev_spin == bull.spin:
      mod = 1
    bull_spin = BULL_SPIN(sum(roll(2)) + mod, bull.spin)
  bull.prev_spin = bull_spin 
  
  # figure out the results
  #@+<< BACK END KICK >>
  #@+node:peckj.20150615154148.1: *5* << BACK END KICK >>
  if bull_maneuver == 'B':
    r = rider.rep + rider.strength + ride_dice
    b = bull.rep + bull.power + style_points
    r = count_successes(roll(r))
    b = count_successes(roll(b))
    delta = b - r
    if delta >= 2:
      if rider.ride_dice == 0:
        return True
      else:
        rider.ride_dice -= 1
        rider.points += 3
    elif delta == 1:
      if rider.ride_dice == 0:
        return True
      else:
        rider.ride_dice -= 1
        rider.points += 3
    elif delta == 0:
      rider.points += 3
    elif delta == -1:
      if lean == False:
        rider.points += 4
      elif lean == bull_maneuver or lean == bull_spin:
        rider.points += 5
      elif lean != bull_maneuver and lean != bull_spin:
        rider.points += 3
      return False
    elif delta <= -2:
      if lean == False:
        rider.points += 4
      elif lean == bull_maneuver or lean == bull_spin:
        rider.points += 5
      elif lean != bull_maneuver and lean != bull_spin:
        rider.points += 3
      rider.points += style_points 
      return False
  #@-<< BACK END KICK >>
  
  #@+<< FRONT END DROP >>
  #@+node:peckj.20150615154153.1: *5* << FRONT END DROP >>
  elif bull_maneuver == 'F':
    r = rider.rep + rider.skill + ride_dice
    b = bull.rep + bull.agility + style_points  
    r = count_successes(roll(r))
    b = count_successes(roll(b))
    delta = b - r
    if delta >= 2:
      if rider.ride_dice == 0:
        return True
      else:
        rider.ride_dice -= 1
        rider.points += 4
    elif delta == 1:
      if rider.ride_dice == 0:
        return True
      else:
        rider.ride_dice -= 1
        rider.points += 4
    elif delta == 0:
      rider.points += 4
    elif delta == -1:
      if lean == False:
        rider.points += 4
      elif lean == bull_maneuver or lean == bull_spin:
        rider.points += 5
      elif lean != bull_maneuver and lean != bull_spin:
        rider.points += 3
      return False
    elif delta <= -2:
      if lean == False:
        rider.points += 5
      elif lean == bull_maneuver or lean == bull_spin:
        rider.points += 6
      elif lean != bull_maneuver and lean != bull_spin:
        rider.points += 4
      rider.points += style_points 
      return False
  #@-<< FRONT END DROP >>
  
  #@+<< SPIN >>
  #@+node:peckj.20150615154144.1: *5* << SPIN >>
  elif bull_maneuver == 'S':
    r = rider.rep + rider.guts + ride_dice
    b = bull.rep + bull.speed + style_points
    r = count_successes(roll(r))
    b = count_successes(roll(b))
    delta = b - r
    if delta >= 2:
      if rider.ride_dice < delta:
        return True
      else:
        rider.ride_dice -= delta
        rider.points += 5
    elif delta == 1:
      if rider.ride_dice == 0:
        return True
      else:
        rider.ride_dice -= 1
        rider.points += 5
    elif delta == 0:
      rider.points += 5
    elif delta == -1:
      if lean == False:
        rider.points += 5
      elif lean == bull_maneuver or lean == bull_spin:
        rider.points += 6
      elif lean != bull_maneuver and lean != bull_spin:
        rider.points += 4
      return False
    elif delta <= -2:
      if lean == False:
        rider.points += 6
      elif lean == bull_maneuver or lean == bull_spin:
        rider.points += 7
      elif lean != bull_maneuver and lean != bull_spin:
        rider.points += 5
      rider.points += style_points 
      return False
  #@-<< SPIN >>
  
  #@+<< SUNFISHING >>
  #@+node:peckj.20150615154158.1: *5* << SUNFISHING >>
  elif bull_maneuver == 'SF':
    r = rider.rep + rider.guts + rider.skill + rider.strength + ride_dice
    b = bull.rep + bull.speed + bull.agility + bull.power + style_points
    r = count_successes(roll(r))
    b = count_successes(roll(b))
    delta = b - r
    if delta >= 2:
      if rider.ride_dice < delta:
        return True
      else:
        rider.ride_dice -= delta
        rider.points += 6
    elif delta == 1:
      if rider.ride_dice < 2:
        return True
      else:
        rider.ride_dice -= 2
        rider.points += 6
    elif delta == 0:
      rider.points += 6
    elif delta == -1:
      if lean == False:
        rider.points += 7
      elif lean == bull_maneuver or lean == bull_spin:
        rider.points += 8
      elif lean != bull_maneuver and lean != bull_spin:
        rider.points += 6
      return False
    elif delta <= -2:
      if lean == False:
        rider.points += 8
      elif lean == bull_maneuver or lean == bull_spin:
        rider.points += 9
      elif lean != bull_maneuver and lean != bull_spin:
        rider.points += 7
      rider.points += style_points 
      return False
  #@-<< SUNFISHING >>

    
    
#@-others

if __name__=='__main__':
  main()
#@-leo
