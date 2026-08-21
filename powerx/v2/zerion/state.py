import uuid,time
class TradeApprovalState:
    def __init__(self):self.items={}
    def create(self,setup):
        i=uuid.uuid4().hex; self.items[i]={"status":"pending_approval","setup":setup,"created_at":time.time()}; return i
    def approve(self,i):
        x=self.items[i]
        if x["status"]!="pending_approval":raise ValueError("not pending")
        x["status"]="approved";x["approved_at"]=time.time();return x
