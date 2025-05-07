// Global AJAX Setup
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrf_token'));
        }
    }
});

// Utility Functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showAlert(message, type = 'success') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    const alertContainer = document.querySelector('.container.mt-3');
    alertContainer.insertAdjacentHTML('beforeend', alertHtml);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = alertContainer.querySelector('.alert');
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

// Order Handling
function placeOrder(productId) {
    const quantity = document.querySelector(`#quantity-${productId}`).value;
    const shippingAddress = document.querySelector(`#shipping-address-${productId}`).value;

    $.ajax({
        url: `/client/order/${productId}`,
        type: 'POST',
        data: {
            quantity: quantity,
            shipping_address: shippingAddress
        },
        success: function(response) {
            showAlert(response.message);
            $(`#orderModal${productId}`).modal('hide');
            setTimeout(() => {
                location.reload();
            }, 1500);
        },
        error: function(xhr) {
            showAlert(xhr.responseJSON.error, 'danger');
        }
    });
}

// Task Management
function markTaskCompleted(taskId) {
    $.ajax({
        url: `/employee/tasks/${taskId}/complete`,
        type: 'POST',
        success: function(response) {
            showAlert('Task marked as completed');
            setTimeout(() => {
                location.reload();
            }, 1500);
        },
        error: function(xhr) {
            showAlert('Error updating task status', 'danger');
        }
    });
}

// Form Validation
document.addEventListener('DOMContentLoaded', function() {
    // Password confirmation validation
    const passwordForm = document.querySelector('form');
    if (passwordForm) {
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm_password');
        
        if (password && confirmPassword) {
            confirmPassword.addEventListener('input', function() {
                if (this.value !== password.value) {
                    this.setCustomValidity('Passwords do not match');
                } else {
                    this.setCustomValidity('');
                }
            });
        }
    }

    // Quantity validation for orders
    const quantityInputs = document.querySelectorAll('input[type="number"][name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('input', function() {
            const max = parseFloat(this.getAttribute('max'));
            const value = parseFloat(this.value);
            
            if (value > max) {
                this.setCustomValidity(`Maximum available quantity is ${max}kg`);
            } else if (value <= 0) {
                this.setCustomValidity('Quantity must be greater than 0');
            } else {
                this.setCustomValidity('');
            }
        });
    });
});

// Dynamic Price Calculation
function updateTotalPrice(productId) {
    const quantityInput = document.querySelector(`#quantity-${productId}`);
    const pricePerKg = parseFloat(document.querySelector(`#price-${productId}`).dataset.price);
    const totalPriceElement = document.querySelector(`#total-price-${productId}`);
    
    if (quantityInput && totalPriceElement) {
        const quantity = parseFloat(quantityInput.value) || 0;
        const totalPrice = (quantity * pricePerKg).toFixed(2);
        totalPriceElement.textContent = `$${totalPrice}`;
    }
}

// Filter Handling
function applyFilters(type) {
    const status = document.getElementById('statusFilter').value;
    const date = document.getElementById('dateFilter').value;
    const url = new URL(window.location.href);
    
    if (status) url.searchParams.set('status', status);
    if (date) url.searchParams.set('date', date);
    
    window.location.href = url.toString();
}

function resetFilters() {
    window.location.href = window.location.pathname;
}

// Initialize Tooltips and Popovers
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

$(document).on('change', '.status-select', function() {
    const orderId = $(this).data('order-id');
    const newStatus = $(this).val();
    
    $.ajax({
        url: `/admin/orders/update-status/${orderId}`,
        type: 'POST',
        data: {
            status: newStatus
        },
        success: function(response) {
            showAlert('Order status updated successfully', 'success');
        },
        error: function(xhr) {
            showAlert('Failed to update order status', 'danger');
            // Reset to previous value
            location.reload();
        }
    });
});

// User Management
$(document).on('click', '.edit-user-btn', function() {
    const userId = $(this).data('user-id');
    const username = $(this).data('username');
    const email = $(this).data('email');
    const role = $(this).data('role');
    const company = $(this).data('company');
    const contact = $(this).data('contact');
    const country = $(this).data('country');
    
    $('#editUserId').val(userId);
    $('#editUsername').val(username);
    $('#editEmail').val(email);
    $('#editRole').val(role);
    $('#editCompanyName').val(company);
    $('#editContactPerson').val(contact);
    $('#editCountry').val(country);
});

$('#editUserForm').on('submit', function(e) {
    e.preventDefault();
    const userId = $('#editUserId').val();
    const formData = new FormData(this);
    
    $.ajax({
        url: `/admin/users/edit/${userId}`,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            $('#editUserModal').modal('hide');
            
            // Update the table row dynamically
            const row = $(`button[data-user-id="${userId}"]`).closest('tr');
            row.find('td:eq(0)').text(formData.get('username'));
            row.find('td:eq(1)').text(formData.get('email'));
            row.find('td:eq(2)').text(formData.get('role'));
            row.find('td:eq(3)').text(formData.get('company_name'));
            row.find('td:eq(4)').text(formData.get('contact_person'));
            row.find('td:eq(5)').text(formData.get('country'));
            
            // Update the edit button data attributes
            const editBtn = row.find('.edit-user-btn');
            editBtn.data('username', formData.get('username'));
            editBtn.data('email', formData.get('email'));
            editBtn.data('role', formData.get('role'));
            editBtn.data('company', formData.get('company_name'));
            editBtn.data('contact', formData.get('contact_person'));
            editBtn.data('country', formData.get('country'));
            
            showAlert('User updated successfully', 'success');
        },
        error: function(xhr) {
            const error = xhr.responseJSON ? xhr.responseJSON.error : 'Failed to update user';
            showAlert(error, 'danger');
        }
    });
});

// Similarly update the toggle status functionality
$(document).on('click', '.toggle-status-btn', function() {
    const btn = $(this);
    const userId = btn.data('user-id');
    const action = btn.data('action');
    
    $.ajax({
        url: `/admin/users/${action}/${userId}`,
        type: 'POST',
        success: function(response) {
            // Update button state without page reload
            if (action === 'activate') {
                btn.text('Deactivate')
                   .removeClass('btn-outline-success')
                   .addClass('btn-outline-danger')
                   .data('action', 'deactivate');
            } else {
                btn.text('Activate')
                   .removeClass('btn-outline-danger')
                   .addClass('btn-outline-success')
                   .data('action', 'activate');
            }
            showAlert(`User ${action}d successfully`, 'success');
        },
        error: function(xhr) {
            showAlert(`Failed to ${action} user`, 'danger');
        }
    });
});

