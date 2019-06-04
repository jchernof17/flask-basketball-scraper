from __future__ import division
from flask import Flask, render_template
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
import requests
class Game():
    def __init__(self, date):
        day = date[0]
        month = date[1]
        year = date[2]
        self.game_scores = client.player_box_scores(day=day, month=month, year=year)

    def getPerformances(self):
        return self.game_scores

    def getPoints(self, player):
        return player['made_three_point_field_goals'] + 2 * player['made_field_goals'] + player['made_free_throws']

    def createTableRows(self):
        if (not self.game_scores):
            return 'Unable to find any players who played on that date.'
        overall_html = '<table><tr><td>Player</td><td>Minutes</td><td>Points</td></tr>'
        for player in self.game_scores:
            name = player['name']
            minutes = str(round(player['seconds_played'] / 60))
            points = str(self.getPoints(player))
            row_html = '<tr><td>' + name + '</td><td>' + minutes + '</td><td>' + points + '</td></tr>' 
            overall_html += row_html
        return overall_html + '</table>'
    