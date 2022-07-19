import random


class People:
    attack = 0
    defence = 0
    HP_max = 100
    HP = 0
    speed = 0
    stunned = False
    broken = 0

    def __init__(self):
        pass

    def round(self, rounds, people):  # return -1 for self lost, 1 for opponent lost, 0 for peace
        self.checkBroken()
        if not self.isAlive():
            return -1
        return self.action(rounds, people)

    def action(self, rounds, people):
        pass  # return -1 for self lost, 1 for opponent lost

    def normal_attack(self, rounds, people):
        if not self.stunned:
            people.beingAttacked(self.attack, self)
        else:
            self.HP -= self.attack - self.defence
            self.recover()

    def skill1(self, rounds, people):
        pass

    def skill2(self, rounds, people):
        pass

    def beingAttacked(self, damage, people):
        if damage > people.defence:
            self.HP -= damage - self.defence

    def isStunned(self):
        return self.stunned

    def stun(self):
        self.stunned = True

    def recover(self):
        self.stunned = False

    def checkBroken(self):
        if self.broken > 0:
            self.HP -= 4
            self.broken -= 1

    def isAlive(self):
        if self.HP > 0:
            return True
        else:
            return False


class Kevin(People):
    attack = 20
    defence = 11
    HP = 100
    speed = 21
    stunned = False

    def action(self, rounds, people):
        d1 = self.skill1(rounds, people)
        if d1 == 0:
            return self.normal_attack(rounds, people)
        else:
            people.beingAttacked(d1 + people.defence, self)
            d2 = self.skill2(rounds, people)
            if d2 == 100:
                return 1
            if not people.isAlive():
                return 1
            return 0

    def normal_attack(self, rounds, people):
        if not self.stunned:
            people.beingAttacked(self.attack, self)
            d2 = self.skill2(rounds, people)
            if d2 == 100:
                return 1
            if not people.isAlive():
                return 1
            return 0
        else:
            self.HP -= self.attack - self.defence
            self.recover()
            if not self.isAlive():
                return -1
            return 0

    def skill1(self, rounds, people):
        if rounds % 3 == 0:
            self.attack += 5
            return 25
        else:
            return 0

    def skill2(self, rounds, people):
        if people.HP < people.HP_max * 0.3:
            if random.random() < 0.3:
                return 100
        return 0


class V2v(People):
    attack = 20
    defence = 12
    HP = 100
    speed = 25
    stunned = False
    activate = False

    def action(self, rounds, people):
        self.skill2(rounds, people)
        d1 = self.skill1(rounds, people)
        if d1 == 0:
            people.beingAttacked(self.attack, self)
        else:
            people.beingAttacked(int(d1), self)
        if people.HP < 0:
            return 1
        return 0

    def skill1(self, rounds, people):
        if rounds % 3 == 0:
            people.stun()
            return self.attack
        return 0

    def skill2(self, rounds, people):
        if self.HP < 31 and not self.activate:
            self.HP += int(random.random() * 10 + 10)
            people.HP += int(random.random() * 10 + 10)
            self.attack += int(13 * random.random() + 2)
            self.activate = True
        return 0


class Kosmo(People):
    attack = 19
    defence = 11
    HP = 100
    speed = 19
    stunned = False
    activate = False

    def action(self, rounds, people):
        d1 = self.skill1(rounds, people)
        if d1 == 0:
            self.normal_attack(rounds, people)
        if not people.isAlive():
            return 1
        return 0

    def normal_attack(self, rounds, people):
        if not self.stunned:
            people.beingAttacked(self.attack, self)
            if random.random() < 0.15:
                people.broken = 3
            if not people.isAlive():
                return 1
            return 0
        else:
            self.HP -= self.attack - self.defence
            self.recover()
            if random.random() < 0.15:
                self.broken = 3
            if not self.isAlive():
                return -1
            return 0

    def skill1(self, rounds, people):
        if rounds % 2 == 0:
            attack = 0
            for i in range(4):
                attack += int(random.random() * 11 + 11)
                if people.broken > 0:
                    attack += 3
                else:
                    if random.random() < 0.15:
                        people.broken = 3
                if attack - people.defence > 0:
                    people.beingAttacked(attack, self)
                attack = 0
            return 1
        return 0


class Griseo(People):
    attack = 16
    defence = 11
    HP = 100
    speed = 18
    stunned = False
    max_defence = 21
    shield = 0

    def action(self, rounds, people):
        if rounds % 3 == 0:
            self.skill1(rounds, people)
        else:
            self.normal_attack(rounds, people)
        if random.random() < 0.4 and self.defence < self.max_defence:
            self.defence += 2
        if not people.isAlive():
            return 1
        if not self.isAlive():
            return -1
        return 0

    def skill1(self, rounds, people):
        if self.shield > 0:
            self.shield = 15
            people.beingAttacked(int(self.defence), self)
        else:
            self.shield = 15

    def beingAttacked(self, damage, people):
        real_damage = damage - self.defence
        if real_damage > 0:
            if self.shield == 0:
                self.HP -= real_damage
            else:
                if real_damage >= self.shield:
                    self.HP -= real_damage - self.shield
                    self.shield = 0
                    people.beingAttacked(int(self.defence*(2*random.random()+2)), self)

                else:
                    self.shield -= real_damage


class Pardofelis(People):
    attack = 17
    defence = 10
    HP = 100
    speed = 24
    stunned = False

    def action(self, rounds, people):
        if rounds % 3 == 0:
            self.skill1(rounds, people)
        else:
            self.normal_attack(rounds, people)
        if random.random() < 0.3:
            people.beingAttacked(30, self)
        if not people.isAlive():
            return 1
        if not self.isAlive():
            return -1
        return 0

    def skill1(self, rounds, people):
        HP_before = people.HP
        people.beingAttacked(30, self)
        HP_after = people.HP
        self.HP += (HP_before - HP_after)
        if self.HP > 100:
            self.HP = 100


def fight(left, right, rounds):
    if left.speed < right.speed:
        r2 = right.round(rounds, left)
        if r2 == 0:
            r1 = left.round(rounds, right)
            if r1 == 0:
                return 0
            elif r1 == -1:
                return 2
            else:
                return 1
        elif r2 == -1:
            return 1
        else:
            return 2
    else:
        r1 = left.round(rounds, right)
        if r1 == 0:
            r2 = right.round(rounds, left)
            if r2 == 0:
                return 0
            elif r2 == -1:
                return 1
            else:
                return 2
        elif r1 == -1:
            return 2
        else:
            return 1


def game():
    kevin_wins = 0
    v2v_wins = 0
    kosmo_wins = 0
    griseo_wins = 0
    pardofelis_wins = 0
    for i in range(1000):
        rounds = 1
        kevin = Kevin()
        v2v = V2v()
        kosmo = Kosmo()
        griseo = Griseo()
        pardofelis = Pardofelis()
        result = 0
        while result == 0:
            result = fight(griseo, pardofelis, rounds)
            # print("rounds: ", rounds, 'griseo HP', griseo.HP)
            print("rounds: ", rounds, 'griseo def', griseo.defence)
            # print("rounds: ", rounds, 'griseo shield', griseo.shield)
            # print("rounds: ", rounds, 'pardo HP', pardofelis.HP)
            rounds += 1
        if result == 1:
            griseo_wins += 1
        else:
            pardofelis_wins += 1
    print('griseo win ', griseo_wins, ' times')
    print('pardofelis win ', pardofelis_wins, ' times')


if __name__ == '__main__':
    game()
