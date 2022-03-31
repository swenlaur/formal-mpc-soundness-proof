theory DataTypes
  imports Main
begin

(* Types made up for the project *)
typedecl message
typedecl partyID
typedecl functionalityID
typedecl portNumber
typedecl messageIndex
typedecl moduleType

(* Types from the Python code *)
(* code.py *)
typedecl code

(* instance_labels.py *)
typedecl instanceLabel
typedecl nullInstanceLabel
(* In Python, this inherits from IL
   Sven: nullInstanceLabel is a specific instance that points to shared
   variables in the state
*)

(* values.py *)
typedecl valueType
typedecl valueTypeLabel
(* Sven: We have values of different types and valueTypeLable is a label for values *)

(* memory_locations.py *)
typedecl memoryLocation
typedecl pinnedMemoryLocation
(* Inheritance
  Sven: Pinned memory location is a specific memory location which is used
  to address shared memory
 *)

(* instance_state.py *)
(*datatype instanceState = IS ? ? ? *)
(* nested map / two-arg function option *)
(* Sven: As in semantics it is a partial function ValueType --> MemoryLocation --> Value  *)


(* protocol_description.py *)
datatype protocolDescription = PD "code list"
(* Sven:
  Protocol is defined by giving the code for all participants thats why this is list
  Code itself is a list of instructions
*)

(* write_instructions.py *)
datatype WriteInstructions = WI "(portNumber × message) list"

end
