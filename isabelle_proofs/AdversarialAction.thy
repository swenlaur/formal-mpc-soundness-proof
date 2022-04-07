theory AdversarialAction
  imports Main DataTypes
begin

(* Swen:
   From technical viewpoint we can have only one data type for clock buffer
   or even one buffer action

record bufferAction =
  party :: partyID
  functionality :: functionalityID
  direction :: {incoming| outgoing}
  action :: {clock|peek}
  msgIndex :: messageIndex

  This means more explicit casing

  if action.action == 'clock' and action.direction == 'incoming':
      # clock incoming buffers

  source and target fields are bad names since these would be in reverse
  for incoming and outcoming actions

J: thanks! Incorporated it
  
*)

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
