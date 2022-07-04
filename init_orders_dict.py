import pickle

orders_dict = {
	"timestamp": -1,
	"strategy0_last_position_order_id": -1,
	"strategy0_last_take_profit_order_id": -1,
	"strategy0_last_stop_loss_order_id": -1,
	"strategy1_last_position_order_id": -1,
	"strategy1_last_take_profit_order_id": -1,
	"strategy1_last_stop_loss_order_id": -1,
	"strategy2_last_position_order_id": -1,
	"strategy2_last_take_profit_order_id": -1,
	"strategy2_last_stop_loss_order_id": -1,
	"strategy3_last_position_order_id": -1,
	"strategy3_last_take_profit_order_id": -1,
	"strategy3_last_stop_loss_order_id": -1
}

pickle.dump(orders_dict, open("orders_dict.pkl", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
