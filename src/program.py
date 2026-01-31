import re
from rich.console import Console
from .pack import Pack, PackManager, TQuestion, Packages
from .modules import points, health

console = Console(color_system='truecolor')


class Program:
    def __init__(self) -> None:
        self.pm = PackManager()
        self.pm.load()

        self.qs = self.pm.get_all_questions()
        self.tags = self.pm.get_all_tags()
        
        self.orders = list[str]()
        for name, tag in self.tags.items():
            v = tag['values']
            self.orders.extend(v)
        #

        Packages['console'] = console
        Packages['points'] = points
        Packages['health'] = health

        self.run()
    #

    def question(self, q: TQuestion, tries: int = -2):
        if health.get() <= 0:
            return 'break'
        if tries == -2:
            tries = q.get('tries', -1)
        events = q.get('on', {})
        correct = False

        if q.get('type', 'literal') == 'literal':
        
            err, out = ("#d12121", "#2784c6")
            color = "#52A926"
            name = q['name']
        
            console.print(f"[{out}]>[/] [{color}]{name}[/]")
        
            color = "#9E9E9E"
        
            guess = console.input(f"[{out}]<[/] [{color}]Answer[/]: ")
        
            answer = q['answer']

            correct = re.match(fr"\s*{answer}\s*", guess, re.IGNORECASE) != None
        #

        if correct:
            console.print('Correct', style="#1a81f8")
            success = events.get('success', None)
            if not success:
                points.sum(1)
            else:
                self.pm.run_event(success)
            #
        else:
            console.print('Incorrect', style='#d31818')
            failed = events.get('failed', None)
            if not failed:
                health.damage()
            else:
                self.pm.run_event(failed)
            #
            
            if q.get("retry", False) and tries != 0:
                if tries > -1:
                    console.print(f'You have [bold]{tries}[/] tries left.', style="#ff6767")
                    self.question(q, tries - 1)
                elif tries == -1:
                    self.question(q, -1)
                #
            #
        #

    def run(self):
        for question in self.orders:
            
            q = self.pm.get_question(question)
            res = self.question(q)
            if res == 'break': 
                console.print('You lose!', style='#d31818')
                break
            
        #
        console.print("")
        console.print(f'You have [bold]{points.get()}[/] points and [bold]{health.get()}[/] health left.', style="#1a81f8")
    #

Program()