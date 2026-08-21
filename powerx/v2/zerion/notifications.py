def build_trade_notification(intent,setup,evaluation,approval_id):
 return {'type':'zerion_trade_opportunity','approval_id':approval_id,'symbol':intent.symbol,'planned_loss':evaluation['risk'],'potential_reward':evaluation['reward'],'confidence':evaluation['confidence'],'message':'Eligible setup found. Approval required before live order.'}
