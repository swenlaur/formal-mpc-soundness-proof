theory AdversarialAction
  imports Main DataTypes
begin

(*Sven said we should synchronize our nomenclature, but I'm not sure how to do that exactly,
but I'll aim to be really clear, at least. *)

(* Sven has a separate "datatypes" folder. That doesn't exactly jive here? *)
(* The Datatypes are quite interesting, but also a lot of them are empty?*)

record clockBuffer = 
  bufferSource :: partyID 
  bufferTarget :: functionalityID
  bufferMsgIndex :: messageIndex

record corruptParty =
  corruptPartyID :: partyID

record invokeEnvironment = 
  invokeMessage :: message

record  sendMessage =
  sendSource :: nat
  sendTarget :: nat
  sendMessage :: message

(*Here's the thing here: sendSource behaves as partyID or portNumber,
depending on whether we're sending an incoming or outgoing message.

So it's either like this (generic), or I'll split it as follows:

record sendIncomingMessage =
  sendISource :: portNumber
  sendITarget :: partyID
  sendIMessage :: message

record sendOutgoingMessage =
  sendOSource :: partyID
  sendOTarget :: portNumber
  sendOMessage :: message *)


record queryFunctionality = 
  queryTarget :: functionalityID
  queryModule :: moduleType
  queryInstance :: string
 (* instanceLabel (* What kind of a thing should instanceLabel be?  *)*)
  queryMessage :: message


datatype adversarialAction =
  ClockIncomingBuffer clockBuffer | 
  ClockOutgoingBuffer clockBuffer |
  CorruptParty corruptParty |
  SendOutgoingMessage sendMessage |
  SendIncomingMessage sendMessage |
  InvokeEnvironment invokeEnvironment |
  QueryFunctionality queryFunctionality
(* ? *)

end