theory DataTypes
  imports Main
begin
type_synonym message = "bool list"
type_synonym partyID = nat
type_synonym functionalityID = nat
type_synonym portNumber = nat
type_synonym messageIndex = nat
type_synonym moduleType = char

(*the data_types material
 (code, instance labels, instance state, memory locations, 
protocol descriptions, values, write instructions) 
is highly unclear. What kinds of types should they be?
What does it mean that most of them are empty?  *)
type_synonym writeInstructions = "(portNumber \<times> message) list"
end
