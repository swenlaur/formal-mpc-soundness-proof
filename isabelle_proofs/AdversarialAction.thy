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
 
*)

datatype dir = Incoming | Outgoing
datatype act = Clock | Peek

record bufferAction =
  party :: partyID
  functionality :: functionalityID
  direction :: dir
  action :: act
  msgIndex :: messageIndex


record queryFunctionality = 
  queryTarget :: functionalityID
  queryModule :: moduleType
  queryInstance :: instanceLabel
  queryMessage :: message


datatype adversarialAction =
  BufferAction bufferAction |
  CorruptParty partyID |
  InvokeEnvironment message |
  QueryFunctionality queryFunctionality

end
