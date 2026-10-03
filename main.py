import sys
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog

# Generated UI files se classes import karein
from main_window import Ui_MainWindow
from evaluate_dialog import Ui_Dialog

# Rules file se point calculation import karein
from evaluate import calculate_player_points


# ------------------------------------
# Evaluate Dialog Class
# ------------------------------------

class EvaluateDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.load_teams()
        self.combo_match.clear()
        self.combo_match.addItem("Match 1")

        # Yeh line honi hi chahiye button ke liye
        self.btn_calc.clicked.connect(self.calculate_score)

    def load_teams(self):
        self.combo_team.clear()
        conn = sqlite3.connect('cricket_game.db')
        cur = conn.cursor()
        cur.execute("SELECT name FROM teams")
        teams = cur.fetchall()
        conn.close()

        for team in teams:
            self.combo_team.addItem(team[0])

    def calculate_score(self):
        print("Calculate button clicked!")  # Check karne ke liye ki click hua ya nahi
        selected_team = self.combo_team.currentText()
        if not selected_team:
            print("No team selected!")
            return

        conn = sqlite3.connect('cricket_game.db')
        cur = conn.cursor()
        cur.execute("SELECT players FROM teams WHERE name=?", (selected_team,))
        row = cur.fetchone()

        if row and row[0]:
            players = [p.strip() for p in row[0].split(',') if p.strip()]
            
            # Sahi names bina kisi space ke:
            self.list_eval_players.clear()
            self.list_eval_points.clear()
            total_score = 0

            for player in players:
                cur.execute("SELECT * FROM match WHERE player=?", (player,))
                match_row = cur.fetchone()
                
                # Apne function ka naam check kar lena (jaise calculate_player_points)
                pts = calculate_player_points(match_row) if match_row else 0

                self.list_eval_players.addItem(player)
                self.list_eval_points.addItem(str(pts))
                total_score += pts

            self.lbl_score.setText(str(total_score))
        else:
            self.list_eval_players.clear()
            self.list_eval_points.clear()
            self.lbl_score.setText("0")
            
        conn.close()


# ------------------------------------
# Main Window Class
# ------------------------------------
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.team_name = ""
        self.pts_avail = 1000
        self.pts_used = 0
        self.selected_players = []
        self.cat_counts = {'BAT': 0, 'BOW': 0, 'AR': 0, 'WK': 0}

        # Menu Connections
        self.actionNEW_team.triggered.connect(self.new_team)
        self.actionOPEN_team.triggered.connect(self.open_team)
        self.actionSAVE_team.triggered.connect(self.save_team)
        self.actionEVALUATE_team.triggered.connect(self.evaluate_team)

        # Radio Filter Connections
        self.rb_bat.toggled.connect(self.filter_players)
        self.rb_bow.toggled.connect(self.filter_players)
        self.rb_ar.toggled.connect(self.filter_players)
        self.rb_wk.toggled.connect(self.filter_players)

        # List Clicks
        self.list_avail.itemDoubleClicked.connect(self.add_player)
        self.list_selected.itemDoubleClicked.connect(self.remove_player)

    def update_counts(self):
        self.lbl_bat_count.setText(f"Batsman (BAT) {self.cat_counts['BAT']}")
        self.lbl_bow_count.setText(f"Bowlers (BOW) {self.cat_counts['BOW']}")
        self.lbl_ar_count.setText(f"Allrounders (AR) {self.cat_counts['AR']}")
        self.lbl_wk_count.setText(f"Wicket-keeper (WK) {self.cat_counts['WK']}")
        self.lbl_pts_avail.setText(f"Points Available {self.pts_avail}")
        self.lbl_pts_used.setText(f"Point Used {self.pts_used}")

    def filter_players(self):
        self.list_avail.clear()
        ctg = 'BAT'
        if self.rb_bow.isChecked(): ctg = 'BWL'
        elif self.rb_ar.isChecked(): ctg = 'AR'
        elif self.rb_wk.isChecked(): ctg = 'WK'

        conn = sqlite3.connect('cricket_game.db')
        cur = conn.cursor()
        cur.execute("SELECT player FROM stats WHERE ctg=?", (ctg,))
        players = cur.fetchall()
        conn.close()

        for p in players:
            if p[0] not in self.selected_players:
                self.list_avail.addItem(p[0])

    def add_player(self, item):
        player_name = item.text()
        conn = sqlite3.connect('cricket_game.db')
        cur = conn.cursor()
        cur.execute("SELECT value, ctg FROM stats WHERE player=?", (player_name,))
        val, ctg = cur.fetchone()
        conn.close()

        cat_key = 'BOW' if ctg == 'BWL' else ctg

        if self.pts_avail < val:
            QMessageBox.warning(self, "Error", "Enough points available nahi hain!")
            return
        if cat_key == 'WK' and self.cat_counts['WK'] >= 1:
            QMessageBox.warning(self, "Error", "Ek se zyada Wicket-keeper nahi le sakte!")
            return

        self.selected_players.append(player_name)
        self.list_selected.addItem(player_name)
        self.list_avail.takeItem(self.list_avail.row(item))

        self.pts_avail -= val
        self.pts_used += val
        self.cat_counts[cat_key] += 1
        self.update_counts()

    def remove_player(self, item):
        player_name = item.text()
        conn = sqlite3.connect('cricket_game.db')
        cur = conn.cursor()
        cur.execute("SELECT value, ctg FROM stats WHERE player=?", (player_name,))
        val, ctg = cur.fetchone()
        conn.close()

        cat_key = 'BOW' if ctg == 'BWL' else ctg

        self.selected_players.remove(player_name)
        self.list_selected.takeItem(self.list_selected.row(item))

        self.pts_avail += val
        self.pts_used -= val
        self.cat_counts[cat_key] -= 1
        self.update_counts()
        self.filter_players()

    def new_team(self):
        text, ok = QInputDialog.getText(self, 'New Team', 'Enter Team Name:')
        if ok and text:
            self.team_name = text
            self.lbl_team_name.setText(f"Team Name: {self.team_name}")
            self.pts_avail = 1000
            self.pts_used = 0
            self.selected_players.clear()
            self.list_selected.clear()
            self.cat_counts = {'BAT': 0, 'BOW': 0, 'AR': 0, 'WK': 0}
            self.update_counts()
            self.filter_players()

    def save_team(self):
        if not self.team_name or len(self.selected_players) == 0:
            QMessageBox.warning(self, "Error", "Team name aur players select karein!")
            return

        players_str = ",".join(self.selected_players)
        conn = sqlite3.connect('cricket_game.db')
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO teams VALUES (?, ?, ?)", (self.team_name, players_str, self.pts_used))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Saved", "Team successfully save ho gayi hai!")

    def open_team(self):
        conn = sqlite3.connect('cricket_game.db')
        cur = conn.cursor()
        cur.execute("SELECT name FROM teams")
        teams = [r[0] for r in cur.fetchall()]
        conn.close()

        if not teams:
            QMessageBox.information(self, "Info", "Koi saved team nahi mili.")
            return

        team, ok = QInputDialog.getItem(self, "Open Team", "Select Team:", teams, 0, False)
        if ok and team:
            self.team_name = team
            self.lbl_team_name.setText(f"Team Name: {self.team_name}")
            conn = sqlite3.connect('cricket_game.db')
            cur = conn.cursor()
            cur.execute("SELECT players, value FROM teams WHERE name=?", (team,))
            players_str, val = cur.fetchone()

            self.selected_players = players_str.split(',')
            self.pts_used = val
            self.pts_avail = 1000 - val
            self.list_selected.clear()
            self.cat_counts = {'BAT': 0, 'BOW': 0, 'AR': 0, 'WK': 0}

            for p in self.selected_players:
                self.list_selected.addItem(p)
                cur.execute("SELECT ctg FROM stats WHERE player=?", (p,))
                ctg = cur.fetchone()[0]
                cat_key = 'BOW' if ctg == 'BWL' else ctg
                self.cat_counts[cat_key] += 1

            conn.close()
            self.update_counts()
            self.filter_players()

    def evaluate_team(self):
        dlg = EvaluateDialog()
        dlg.exec_()


# ------------------------------------
# Application Entry Point
# ------------------------------------
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())