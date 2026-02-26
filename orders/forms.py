from django import forms

# Province / State choices
STATE_CHOICES = [
    ('Punjab', 'Punjab'),
    ('Sindh', 'Sindh'),
    ('KPK', 'KPK'),
    ('Balochistan', 'Balochistan'),
    ('GB' , 'GB')
]


class CheckoutForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition',
            'placeholder': 'Full Name',
        })
    )

    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition',
            'placeholder': 'Phone Number',
        })
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition',
            'placeholder': 'Email Address (optional)',
        })
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition',
            'placeholder': 'Delivery Address',
            'rows': 3,
        })
    )

    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition',
            'placeholder': 'City',
        })
    )

    # 🔽 State / Province dropdown
    state = forms.ChoiceField(
        choices=[('', 'Select Province')] + STATE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition bg-black text-gray-200',
        })
    )

    payment_method = forms.ChoiceField(
        choices=[
            ('cod', 'Cash on Delivery'),
            ('online', 'Online Payment'),
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'text-emerald-600 focus:ring-emerald-500',
        }),
        initial='cod'
    )