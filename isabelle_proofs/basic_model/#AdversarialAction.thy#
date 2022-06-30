theory AdversarialAction
  imports
    Main 
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/data_types/DataTypes"
begin


datatype dir = Incoming | Outgoing
datatype act = Clock | Peek

record buffer_action =
  bufferParty :: party_id
  bufferFunc :: functionality_id
  bufferDirection :: dir
  bufferAction :: act
  bufferInd :: msg_index

(* Env has no Module, no Instance *)
record query_functionality =
  queryTarget :: functionality_id
  queryModule :: module_type
  queryInstance :: instance_label
  queryMessage :: msg

record send_message =
  sendParty :: party_id
  sendFunc :: functionality_id
  sendDir :: dir
  sendMessage :: msg

datatype adv_action =
  Empty |
  CorruptParty party_id |
  BufferAction buffer_action |
  SendMessage send_message |
  QueryFunctionality query_functionality

end
