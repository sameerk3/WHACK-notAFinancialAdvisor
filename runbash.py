from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
import time
import threading
from uagents import Agent, Bureau, Context, Model
from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low


app = FastAPI()

def run_script_for_10_seconds():

    class PaymentRequest(Model):
        wallet_address: str
        amount: int
        denom: str


    class TransactionInfo(Model):
        tx_hash: str


    AMOUNT = 100
    DENOM = "atestfet"

    personal_wallet = Agent(name="personal_wallet", seed="personal_wallet secret phrase")
    dash_wallet = Agent(name="dash_wallet", seed="dash_wallet secret phrase")


    fund_agent_if_low(dash_wallet.wallet.address(), min_balance=AMOUNT)


    @personal_wallet.on_interval(period=10.0)
    async def request_funds(ctx: Context):
        await ctx.send(dash_wallet.address, 
            PaymentRequest(
                wallet_address=str(personal_wallet.wallet.address()), amount=AMOUNT, denom=DENOM
            ),
        )


    @personal_wallet.on_message(model=TransactionInfo)
    async def confirm_transaction(ctx: Context, sender: str, msg: TransactionInfo):
        ctx.logger.info(f"Received transaction info from {sender}: {msg}")
        tx_resp = await wait_for_tx_to_complete(msg.tx_hash, ctx.ledger)

        coin_received = tx_resp.events["coin_received"]
        if (
            coin_received["receiver"] == str(personal_wallet.wallet.address())
            and coin_received["amount"] == f"{AMOUNT}{DENOM}"
        ):
            ctx.logger.info(f"Transaction was successful: {coin_received}")


    @dash_wallet.on_message(model=PaymentRequest, replies=TransactionInfo)
    async def send_payment(ctx: Context, sender: str, msg: PaymentRequest):
        ctx.logger.info(f"Received payment request from {sender}: {msg}")

        # send the payment
        transaction = ctx.ledger.send_tokens(
            msg.wallet_address, msg.amount, msg.denom, dash_wallet.wallet
        )

        # send the tx hash so alice can confirm
        await ctx.send(personal_wallet.address, TransactionInfo(tx_hash=transaction.tx_hash))


    bureau = Bureau()
    bureau.add(personal_wallet)
    bureau.add(dash_wallet)


    if __name__ == "__main__":
        bureau.run()

@app.post("/run-script")
async def run_script(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_script_for_10_seconds)
    return JSONResponse({"message": "Python script started for 10 seconds!"})