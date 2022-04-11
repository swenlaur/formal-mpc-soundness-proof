theory AdversarialAction
  imports Main DataTypes
begin


datatype dir = Incoming | Outgoing
datatype act = Clock | Peek

record buffer_action =
  bufferParty :: party_id
  bufferFunctionality :: functionality_id
  bufferDirection :: dir
  bufferAction :: act
  bufferMsgIndex :: msg_index

record query_functionality = 
  queryTarget :: functionality_id
  queryModule :: module_type
  queryInstance :: instance_label
  queryMessage :: msg

datatype adv_action =
  CorruptParty party_id |
  BufferAction buffer_action |
  InvokeEnvironment msg |
  QueryFunctionality query_functionality

end