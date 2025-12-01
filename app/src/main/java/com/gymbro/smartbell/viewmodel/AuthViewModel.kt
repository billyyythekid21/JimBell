package com.gymbro.smartbell.viewmodel

import androidx.lifecycle.ViewModel
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

class AuthViewModel : ViewModel() {

    private val auth = FirebaseAuth.getInstance()
    private val _authState = MutableStateFlow<AuthState>(AuthState.Idle)
    private val db = FirebaseFirestore.getInstance()
    val authState: StateFlow<AuthState> = _authState

    fun register(email: String, password: String) {
        _authState.value = AuthState.Loading
        auth.createUserWithEmailAndPassword(email, password)
            .addOnCompleteListener { task ->
                if (task.isSuccessful) {
                    val uid = auth.currentUser?.uid ?: return@addOnCompleteListener
                    val userMap = mapOf(
                        "email" to email,
                    )
                    db.collection("users").document(uid).set(userMap)
                        .addOnSuccessListener {
                            _authState.value = AuthState.NewUser
                        }
                        .addOnFailureListener {
                            _authState.value = AuthState.Error("User created but failed to save profile")
                        }
                } else {
                    _authState.value = AuthState.Error(task.exception?.message)
                }
            }
    }

    fun login(email: String, password: String) {
        _authState.value = AuthState.Loading
        auth.signInWithEmailAndPassword(email, password)
            .addOnCompleteListener {
                _authState.value = if (it.isSuccessful) AuthState.Success
                else AuthState.Error(it.exception?.message)
            }
    }

    fun logout() {
        auth.signOut()
        _authState.value = AuthState.Idle
    }
}

sealed class AuthState {
    object Idle : AuthState()
    object Loading : AuthState()
    object Success : AuthState()
    object NewUser : AuthState()
    data class Error(val message: String?) : AuthState()
}