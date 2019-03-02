# Cyber-Physical systems source task implementations

## Network tasks
Using Python, NetworkX and Matplotlib make:

1) develop broadcast model and model "broadcast storm";
2) develop model without storm;
3) estimate needed time for utility structures in Model II;
4) improve Model II to remove utility structures just in time.

Original:

> Використовуючи мову програмування Python 3 і бібліотеку NetworkX
> 1) розробити модель розповсюдження інформаціїї за схемою "broadcast", продемонструвати ефект "broadcast storm";
> 2) розробити покращену модель за схемою "broadcast", яка не призводить до ефекту "broadcast storm";
> 3) оцінити необхідний час життя допоміжних структур для протоколу, що Ви побудували у п. 2;
> 4) удосконалити модель п.2, забезпечивши своєчасне видалення допоміжних структур.

### Instructions

1) dependencies: `python3.6`, `networkx-2.2`, `matplotlib-3`;
2) you **CAN** run `pip install -r requirements.txt` to install versions I have;
3) run `python <script> [--help]` to run any of them.

### 3rd task explanation
...

### 4th task

Interesting results can be seen running this:
`python network-4.py -v=10 -p=0.2 -n=20 -b=0.4 -s=8460`
