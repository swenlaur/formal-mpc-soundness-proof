theory Buffers
imports Main DataTypes
begin

(* helper *)
primrec remove_nth :: "nat => 'a list \<Rightarrow> 'a list" where
"remove_nth n [] = []" |
"remove_nth n (x # xs) = (case n of 0 \<Rightarrow> xs | Suc m \<Rightarrow> x # remove_nth m xs)"

(* =============== *)

record leaky_buffer =
  messages :: "msg list"

definition write_message :: "'a leaky_buffer_scheme \<Rightarrow> msg \<Rightarrow> 'a leaky_buffer_scheme" where
"write_message b m = b\<lparr>messages :=  m # ( messages b)\<rparr>" 

definition clock_message :: "'a leaky_buffer_scheme \<Rightarrow> nat \<Rightarrow> (msg \<times>'a leaky_buffer_scheme) option" where
"clock_message b n = (if n \<ge> length (messages b) then None 
else Some (messages b ! n, b\<lparr>messages := remove_nth n (messages b)\<rparr>))"

definition empty :: "'a leaky_buffer_scheme option  \<Rightarrow> bool" where
"empty b = (case b of None \<Rightarrow> False |
 Some lb \<Rightarrow> (case (messages lb) of [] \<Rightarrow> True | xs \<Rightarrow> False))"

(*What's up with the structure of peek_message? *)
consts peek_message :: "'a leaky_buffer_scheme \<Rightarrow> msg_index \<Rightarrow> msg" 
  (*where
"peek_message b n = leak_function messages b ! n"*)
(* I don't get what the asserts are*)

consts leak_function :: "msg \<Rightarrow> msg"

end
