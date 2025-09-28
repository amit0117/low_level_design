from app.models.user import User
from app.observers.group_observer import GroupSubject
from app.models.expense import Expense
from uuid import uuid4
from heapq import heappush, heappop
from app.models.transaction import Transaction


class Group(GroupSubject):
    def __init__(self, name: str, members: list[User]):
        super().__init__()
        self.id = str(uuid4())
        self.name = name
        self.members: list[User] = members
        self.expenses: list[Expense] = []
        # Add all the members as observers
        for member in members:
            self.add_observer(member)

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_members(self) -> list[User]:
        return self.members.copy()

    def add_member(self, member: User):
        self.members.append(member)
        self.add_observer(member)
        self.notify_observers(message=f"New member '{member.get_name()}' added to group '{self.get_name()}'")

    def remove_member(self, member: User):
        self.members.remove(member)
        self.remove_observer(member)
        # Notify the observers about the removed member
        self.notify_observers(message=f"Member '{member.get_name()}' removed from group '{self.get_name()}'")

    def add_expense(self, expense: Expense):
        self.expenses.append(expense)

        # Update balance sheets based on expense splits
        splits = expense.get_splits()
        paid_by = expense.get_paid_by()

        for split in splits:
            participant = split.get_user()
            amount = split.get_amount()

            # The participant owes the paid_by user this amount
            participant.get_balance_sheet().adjust_balance(paid_by, amount)
            # The paid_by user is owed this amount by the participant
            paid_by.get_balance_sheet().adjust_balance(participant, -amount)

        # Notify only the expense participants, not all group members
        expense.notify_observers(expense, f"New expense '{expense.get_description()}' added to group '{self.get_name()}'")

    def get_expenses(self) -> list[Expense]:
        return self.expenses.copy()

    def simplify_expenses(self):
        # First create the net balances for each member
        net_balances: dict[User, float] = {}
        for expense in self.expenses:
            paid_by = expense.get_paid_by()
            for split in expense.get_splits():
                participant = split.get_user()
                amount = split.get_amount()
                if participant != paid_by:
                    net_balances[paid_by] = net_balances.get(paid_by, 0) + amount
                    net_balances[participant] = net_balances.get(participant, 0) - amount

        # create two max-heap for creditors and debtors (Since python heapq is a min-heap, we need to negate the balance)
        creditors = []
        debtors = []
        for user, balance in net_balances.items():
            # skip if there is no balance
            if balance == 0:
                continue
            # if balance is positive, add to creditors
            if balance > 0:
                heappush(creditors, (-balance, user.get_id(), user))
            else:
                # Don't negate the debit balance because it's already negative and we want to use it as a max-heap
                heappush(debtors, (balance, user.get_id(), user))

        # create the transactions to simplify the debts
        transactions: list[Transaction] = []
        while creditors:
            creditor = heappop(creditors)
            debtor = heappop(debtors)
            amount = min(-1 * creditor[0], -1 * debtor[0])  # -1 is multiplied to make the value positive for debtor
            transaction = Transaction(debtor[2], creditor[2], amount)
            transactions.append(transaction)

            # Re-insert to the heap if there is remaining balance
            if (-1 * creditor[0] - amount) > 0:
                heappush(creditors, (creditor[0] + amount, creditor[1], creditor[2]))
            if (-1 * debtor[0] - amount) > 0:
                heappush(debtors, (debtor[0] + amount, debtor[1], debtor[2]))

        return transactions
