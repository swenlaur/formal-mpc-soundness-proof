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
(* In Python, this inherits from IL *)

(* values.py *)
typedecl valueType
typedecl valueTypeLabel

(* memory_locations.py *)
typedecl memoryLocation 
typedecl pinnedMemoryLocation
 (* Inheritance *)

(* instance_state.py *)
(*datatype instanceState = IS ? ? ? *)
(* nested map / two-arg function option *)


(* protocol_description.py *)
datatype protocolDescription = PD "code list"

(* write_instructions.py *)
datatype WriteInstructions = WI "(portNumber × message) list"

end
