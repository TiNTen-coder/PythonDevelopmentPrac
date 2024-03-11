import cmd
import calendar
import shlex

class Calen(cmd.Cmd):
    """Dumb echo command REPL"""
    prompt = "Calendar :-> "
    
    def do_EOF(self, args):
        return True

    def emptyline(self):
        pass

    def do_prmonth(self, args):
        """Print a month's calendar. Usage: prmonth <year> <month>"""
        try:
            year, month = map(int, shlex.split(args))
            calendar.TextCalendar().prmonth(year, month)
        except (ValueError, TypeError, IndexError):
            print("Invalid input. Usage: prmonth <year> <month>")
    
    def do_pryear(self, args):
        """Print a year's calendar. Usage: pryear <year>"""
        try:
            year = int(args)
            calendar.TextCalendar().pryear(year)
        except (ValueError, TypeError):
            print("Invalid input. Usage: pryear <year>")

        


if __name__ == '__main__':
    Calen().cmdloop()
