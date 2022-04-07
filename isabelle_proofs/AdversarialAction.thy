theory AdversarialAction
  imports Main DataTypes
begin

datatype dir = Incoming | Outgoing
datatype act = Clock | Peek

record buffer_action =
  party :: party_id
  functionality :: functionality_id
  direction :: dir
  action :: act
  msgIndex :: msg_index


record query_functionality = 
  queryTarget :: functionality_id
  queryModule :: module_type
  queryInstance :: instance_label
  queryMessage :: msg


datatype adv_action =
  BufferAction buffer_action |
  CorruptParty party_id |
  InvokeEnvironment msg |
  QueryFunctionality query_functionality

end
