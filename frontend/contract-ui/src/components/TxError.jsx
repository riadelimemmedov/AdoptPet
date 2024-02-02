//*TxError
export function TxError(){
    //return jsx to client
    return(
        <>
            <div className="message-warning" role="alert">
                <div>Error sending transaction: Something went wrong...</div>
                <br />
                <button type="button dismiss-button" className="close">
                    <div>Dismiss</div>
                </button>
            </div>
        </>
    )
}
