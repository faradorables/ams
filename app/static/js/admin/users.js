let _page, _limit, _total_data;

function numberWithCommas(number) {
    var parts = number.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}
$(document).ready(function() {
  $("#total_wallet").each(function() {
    var num = $(this).text();
    var commaNum = numberWithCommas(num);
    $(this).text(commaNum);
  });
});

function _users(){
  $(document).ready(function () {
    _page = 0;
    _limit = 25;
    showBy();
    _loading(0);
    // $('#modalDetail').modal('show')
  });
}

function showBy() {
  var show = document.getElementById("showBy");
  if (show.value == "all"){
        _users_list(_page);
    }else if (show.value == "upgraded"){
      _users_upgraded(_page);
    }else if (show.value == "suspended"){
      _users_suspended(_page);
    }
}
// ========================================================
// users LIST
// ========================================================

// CALL THE users
function _users_list(page){
  _loading(1);
  $.post('/api/v1/ams/users',{
      'id': userData['id'],
      'token': userData['token'],
      'status': 0,
      'page': page,
      'sector_id': $('#sector_id').val(),
  }, function (e) {
    let i;
    if(e['status'] === '00'){
      _total_data = e.count_user.total_user;
      $('.small_data').text((_page*_limit)+1)
      let _big_data = (_page+1)*_limit;
      console.log('test');
      let _max = parseInt(_total_data/_limit);
      if(_big_data >= _total_data){
        console.log('test');
        _big_data = _total_data;
      }
      _check_arrow(_max);
      $('.big_data').text(_big_data);
      $('#total_users, .total_data').text(_total_data);
      $('#total_active_users').text(e.count_user.active_user);
      $('#total_wallet').text('Rp ' + e.total_wallet);
      $('#total_trx').text('Rp ' + e.total_trx);
      $('#data_body').empty();
      if(e.data.length > 0){
        for(i=0; i < e.data.length; i++){
          _users_append(e.data[i], i+1);
          // console.log(e.data);
        }
      }else{
        $('#data_body').append(
          '<div class="_notif_menu"><i class="fa fa-exclamation-triangle"></i>User dari sektor ini belum tersedia.</div>'
        )
      }
    }else{
      notif('danger', 'System Error!', e.message);
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

function _users_upgraded(page){
  _loading(1);
  $.post('/api/v1/ams/users_upgraded',{
      'id': userData['id'],
      'token': userData['token'],
      'status': 0,
      'page': page,
      'sector_id': $('#sector_id').val(),
  }, function (e) {
    let i;
    if(e['status'] === '00'){
      _total_data = e.count_user.total_user;
      $('.small_data').text((_page*_limit)+1)
      let _big_data = (_page+1)*_limit;
      console.log('test');
      let _max = parseInt(_total_data/_limit);
      if(_big_data >= _total_data){
        console.log('test');
        _big_data = _total_data;
      }
      _check_arrow(_max);
      $('.big_data').text(_big_data);
      $('#total_users, .total_data').text(_total_data);
      $('#total_active_users').text(e.count_user.active_user);
      $('#total_wallet').text('Rp ' + e.total_wallet);
      $('#total_trx').text('Rp ' + e.total_trx);
      $('#data_body').empty();
      if(e.data.length > 0){
        for(i=0; i < e.data.length; i++){
          _users_append(e.data[i], i+1);
          // console.log(e.data);
        }
      }else{
        $('#data_body').append(
          '<div class="_notif_menu"><i class="fa fa-exclamation-triangle"></i>User dari sektor ini belum tersedia.</div>'
        )
      }
    }else{
      notif('danger', 'System Error!', e.message);
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

function _users_suspended(page){
  _loading(1);
  $.post('/api/v1/ams/users_suspended',{
      'id': userData['id'],
      'token': userData['token'],
      'status': 0,
      'page': page,
      'sector_id': $('#sector_id').val(),
  }, function (e) {
    let i;
    if(e['status'] === '00'){
      _total_data = e.count_user.total_user;
      $('.small_data').text((_page*_limit)+1)
      let _big_data = (_page+1)*_limit;
      console.log('test');
      let _max = parseInt(_total_data/_limit);
      if(_big_data >= _total_data){
        console.log('test');
        _big_data = _total_data;
      }
      _check_arrow(_max);
      $('.big_data').text(_big_data);
      $('#total_users, .total_data').text(_total_data);
      $('#total_active_users').text(e.count_user.active_user);
      $('#total_wallet').text('Rp ' + e.total_wallet);
      $('#total_trx').text('Rp ' + e.total_trx);
      $('#data_body').empty();
      if(e.data.length > 0){
        for(i=0; i < e.data.length; i++){
          _users_append(e.data[i], i+1);
          // console.log(e.data);
        }
      }else{
        $('#data_body').append(
          '<div class="_notif_menu"><i class="fa fa-exclamation-triangle"></i>User dari sektor ini belum tersedia.</div>'
        )
      }
    }else{
      notif('danger', 'System Error!', e.message);
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

// NEXT PAGE BUTTON
function _next_page(){
  if((_page + 1)*25<_total_data){
    _page += 1;
    _users_list(_page)
  }
}

// PREVIOUS PAGE BUTTON
function _prev_page(){
  if(_page > 0){
    _page -= 1;
    _users_list(_page)
  }
}

// CHECKING THE PAGE AND THE ARROW
function _check_arrow(max){
  $('.left_arrow, .right_arrow').removeClass('disabled');
  if(_page === 0 && _page != max){
    $('.left_arrow').addClass('disabled');
  }else if(_page === 0 && _page === max){
    $('.left_arrow, .right_arrow').addClass('disabled');
  }else if(_page === max){
    $('.right_arrow').addClass('disabled');
  }
}

function _users_transaction(id){
  $.post('/api/v1/ams/history',{
      'id': userData['id'],
      'token': userData['token'],
      'status': 0,
      'user_id': id,
      'skip':0
  }, function (e) {
    let i;
    if(e['status'] === '00'){
      $('#data_trx').empty();
      if(e.data.length > 0){
        for(i=0; i < e.data.length; i++){
          _trx_append(e.data[i], i+1);
        }
        for(i=0; i < e.data.length; i++){
          _trx_all_append(e.data[i], i+1);
        }
      }else{
        $('#data_trx').append(
          '<div class="_notif_menu"><i class="fa fa-exclamation-triangle"></i>User ini belum memiliki riwayat transaksi</div>'
        )
      }
    }else{
      notif('danger', 'System Error!', e.message);
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

// APPENDING THE users
function _users_append(data, i){
  // upgradeDetail(data.id_upgrade);
  $('#data_body').append(
    '<div onclick="modalDetail('+data.id+')">' +
    '<div class="no">' + i + '</div>' +
    '<div><div class="profilePicture"></div></div>' +
    '<div class="name">' + data.name + '</div>' +
    '<div class="email">' + data.email + '</div>' +
    '<div class="phone">' + data.phone_number + '</div>' +
    '<div class="value">Rp ' + data.wallet + '</div>' +
    '<div class="option">' +
    '<a><i class="fas fa-info-circle"></i></a>' +
    '<a><i class="fas fa-ban"></i></a>' +
    '</div>' +
    '</div>'
  )
}

function _trx_append(data, i){
  console.log(data)
  $('#data_trx').append(
    // '<table class="table table-hover">'+
    '<tr onclick="translog_detail_modal(\'' + data.id + '\')">'+
    '<td>' + i + '</td>' +
    '<td>' + "Rp. " + data.amount + '</td>' +
    '<td>' + data.product_category_name + '</td>' +
    '<td>' + data.product_type_name + '</td>' +
    '<td>' + data.date + '</td>' +
    '</tr>'+
    '</table>'
  )
}

function _trx_all_append(data, i){
  $('#data_trx_all').append(
    '<tr>'+
    '<td>' + i + '</td>' +
    '<td>' + "Rp. " + data.amount + '</td>' +
    '<td>' + data.product_category_name + '</td>' +
    '<td>' + data.product_type_name + '</td>' +
    '<td>' + data.date + '</td>' +
    '</tr>'+
    '</table>'
  )
}

function modalDetail(id){
  _loading(1);
  $.post('/api/v1/ams/userdetail',{
      'id_admin': userData['id'],
      'token': userData['token'],
      'status': 0,
      'user_id': id,
  }, function (e) {
    let i;
      if(e['status'] === '00'){
        if (id > 0){
          _users_transaction(id);
          $('#detail_name').text(e.id.name);
          $('#detail_phone').text(e.id.phone);
          $('#detail_email').text(e.id.email);
          $('#user_total_wallet').text('Rp ' + e.id.wallet);
          $('#user_total_obu').text(+ e.id.total_obu);
          $('#user_total_trx').text('Rp ' + e.id.user_trx);
          if(e.id.status_upgrade == 1){
            $('#detail_upgrade').text('Pending Upgrade')
          }else if(e.id.status_upgrade==2){
            $('#detail_upgrade').text('Upgraded')
          }else if(e.id.status_upgrade==3){
            $('#detail_upgrade').text('Rejected Upgrade')
          }else{
            $('#detail_upgrade').text('Not Upgrade')
          }
        }else{
          notif('danger', 'System Error!', 'user tidak terdaftar')
        }
    }else{
      notif('danger', 'System Error!', e.message);
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });


  $('#modalDetail').modal('show');
}

$('#modalDetail').on('shown.bs.modal', function () {
  $(this).css({'padding': '0'})
})

function trx_all_modal(){
  $('#trxallmodal').modal('show');
}

$('#trxallmodal').on('shown.bs.modal', function () {
  $(this).css({'padding': '0'})
})

function translog_detail_modal(_id){
_loading(1);
$.post('/api/v1/ams/trx_log',{
    'id': userData['id'],
    'token': userData['token'],
    'status': 1,
    '_id': _id
}, function (e) {
  let i;
    if(e['status'] === '00'){
      $('#user_id').text(e.data.user_id);
      $('#name').text(e.data.name);
      $('#type_name').text(e.data.type_name);
      $('#amount').text('Rp.'+e.data.amount);
      $('#date').text(e.data.date);
      $('#uid').text(e.data.uid);
      $('#product_category_name').text(e.data.product_category_name);
      $('#product_detail_name').text(e.data.product_detail_name);
      $('#product_type_name').text(e.data.product_type_name);
      $('#provider').text(e.data.provider);
      $('#ref_id').text(e.data.ref_id);
      $('#refca').text(e.data.refca);
      $('#refsb').text(e.data.refsb);
      $('#serialno').text(e.data.serialno);
      console.log(e);
  }else{
    notif('danger', 'System Error!', e.message);
  }
}).fail(function(){
  notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
}).done(function(){
  _loading(0);
});

  $('#translogdetailmodal').modal('show');
}

$('#translogdetailmodal').on('shown.bs.modal', function () {
  $(this).css({'padding': '0'})
})
